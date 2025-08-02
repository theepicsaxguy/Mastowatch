#!/bin/bash
set -e

# Mastodon API Client Update Script
# This script automates the process of updating the Mastodon OpenAPI specification
# and regenerating the typed Python client.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SPECS_DIR="$PROJECT_DIR/specs"
CLIENT_DIR="$PROJECT_DIR/app/clients/mastodon"

echo "=== Mastodon API Client Update Script ==="
echo "Project directory: $PROJECT_DIR"
echo ""

# Create specs directory if it doesn't exist
mkdir -p "$SPECS_DIR"

# Function to download the latest OpenAPI spec
download_spec() {
    echo "📥 Downloading latest Mastodon OpenAPI specification..."
    
    # Primary source (the blob URL you provided)
    SPEC_URL="https://abraham.github.io/2d1b5745-0dd7-41ce-b651-97082ae9b878"
    
    # Backup source
    BACKUP_URL="https://abraham.github.io/mastodon-openapi/openapi.json"
    
    if curl -f -L "$SPEC_URL" -o "$SPECS_DIR/openapi.json.tmp"; then
        echo "✅ Successfully downloaded from primary source"
        mv "$SPECS_DIR/openapi.json.tmp" "$SPECS_DIR/openapi.json"
    elif curl -f -L "$BACKUP_URL" -o "$SPECS_DIR/openapi.json.tmp"; then
        echo "⚠️  Primary source failed, using backup source"
        mv "$SPECS_DIR/openapi.json.tmp" "$SPECS_DIR/openapi.json"
    else
        echo "❌ Failed to download OpenAPI specification from both sources"
        exit 1
    fi
}

# Function to validate the downloaded spec
validate_spec() {
    echo ""
    echo "🔍 Validating OpenAPI specification..."
    
    # Check if file exists and is not empty
    if [[ ! -f "$SPECS_DIR/openapi.json" || ! -s "$SPECS_DIR/openapi.json" ]]; then
        echo "❌ OpenAPI specification file is missing or empty"
        exit 1
    fi
    
    # Check if it's valid JSON
    if ! python3 -c "import json; json.load(open('$SPECS_DIR/openapi.json'))" 2>/dev/null; then
        echo "❌ OpenAPI specification is not valid JSON"
        exit 1
    fi
    
    # Check if it has required OpenAPI fields
    if ! python3 -c "
import json
spec = json.load(open('$SPECS_DIR/openapi.json'))
assert 'openapi' in spec, 'Missing openapi field'
assert 'info' in spec, 'Missing info field'
assert 'paths' in spec, 'Missing paths field'
print(f\"OpenAPI version: {spec['openapi']}\")
print(f\"API title: {spec['info']['title']}\")
print(f\"API version: {spec['info']['version']}\")
print(f\"Number of paths: {len(spec['paths'])}\")
"; then
        echo "❌ OpenAPI specification is missing required fields"
        exit 1
    fi
    
    echo "✅ OpenAPI specification is valid"
}

# Function to backup existing client
backup_client() {
    if [[ -d "$CLIENT_DIR" ]]; then
        echo ""
        echo "📦 Backing up existing client..."
        BACKUP_DIR="$CLIENT_DIR.backup.$(date +%Y%m%d_%H%M%S)"
        cp -r "$CLIENT_DIR" "$BACKUP_DIR"
        echo "✅ Backup created at: $BACKUP_DIR"
    fi
}

# Function to generate the new client
generate_client() {
    echo ""
    echo "🔧 Generating new typed Python client..."
    
    # Remove existing client
    if [[ -d "$CLIENT_DIR" ]]; then
        rm -rf "$CLIENT_DIR"
    fi
    
    # Change to project directory for client generation
    cd "$PROJECT_DIR"
    
    # Generate the client
    if openapi-python-client generate --path "$SPECS_DIR/openapi.json" --meta none; then
        echo "✅ Client generation completed"
        
        # Move generated client to correct location
        if [[ -d "mastodon_api_client" ]]; then
            mkdir -p "$(dirname "$CLIENT_DIR")"
            mv "mastodon_api_client" "$CLIENT_DIR"
            echo "✅ Client moved to app/clients/mastodon"
        else
            echo "❌ Generated client directory not found"
            exit 1
        fi
    else
        echo "❌ Client generation failed"
        exit 1
    fi
}

# Function to run basic validation on generated client
validate_client() {
    echo ""
    echo "🧪 Validating generated client..."
    
    # Check if key files exist
    required_files=(
        "$CLIENT_DIR/__init__.py"
        "$CLIENT_DIR/client.py"
        "$CLIENT_DIR/models"
        "$CLIENT_DIR/api"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -e "$file" ]]; then
            echo "❌ Missing required file/directory: $file"
            exit 1
        fi
    done
    
    # Check if we can import the client (basic syntax check)
    cd "$PROJECT_DIR"
    if python3 -c "from app.clients.mastodon import Client, AuthenticatedClient; print('✅ Client imports successfully')" 2>/dev/null; then
        echo "✅ Generated client passes import test"
    else
        echo "⚠️  Generated client has import issues (this may be normal if dependencies aren't installed)"
    fi
}

# Function to show update summary
show_summary() {
    echo ""
    echo "📊 Update Summary"
    echo "=================="
    
    if [[ -f "$SPECS_DIR/openapi.json" ]]; then
        python3 -c "
import json
import os
spec = json.load(open('$SPECS_DIR/openapi.json'))
print(f'OpenAPI Version: {spec[\"openapi\"]}')
print(f'API Version: {spec[\"info\"][\"version\"]}')
print(f'API Title: {spec[\"info\"][\"title\"]}')
print(f'Total Endpoints: {len(spec[\"paths\"])}')
print(f'Spec File Size: {os.path.getsize(\"$SPECS_DIR/openapi.json\")} bytes')
"
    fi
    
    if [[ -d "$CLIENT_DIR" ]]; then
        api_modules=$(find "$CLIENT_DIR/api" -name "*.py" | wc -l)
        model_modules=$(find "$CLIENT_DIR/models" -name "*.py" | wc -l)
        echo "Generated API modules: $api_modules"
        echo "Generated model modules: $model_modules"
    fi
    
    echo ""
    echo "🎉 Update completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Review the generated client for any breaking changes"
    echo "2. Run your tests to ensure compatibility"
    echo "3. Update your code to use new type-safe methods where available"
    echo "4. Consider updating your requirements.txt if needed"
}

# Main execution
main() {
    case "${1:-all}" in
        "download")
            download_spec
            validate_spec
            ;;
        "generate")
            generate_client
            validate_client
            ;;
        "all")
            download_spec
            validate_spec
            backup_client
            generate_client
            validate_client
            show_summary
            ;;
        "help")
            echo "Usage: $0 [download|generate|all|help]"
            echo ""
            echo "Commands:"
            echo "  download  - Download and validate the OpenAPI specification"
            echo "  generate  - Generate the Python client from existing spec"
            echo "  all       - Download spec and generate client (default)"
            echo "  help      - Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
