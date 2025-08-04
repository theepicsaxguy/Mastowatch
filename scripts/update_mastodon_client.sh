#!/bin/bash

# Enhanced Mastodon API Client Management Script
# Uses Git submodule for better version control and reproducibility

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SUBMODULE_PATH="$PROJECT_ROOT/specs/mastodon-openapi"
SCHEMA_SOURCE="$SUBMODULE_PATH/dist/schema.json"
SCHEMA_DEST="$PROJECT_ROOT/specs/openapi.json"
CLIENT_DIR="$PROJECT_ROOT/app/clients/mastodon"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
Mastodon API Client Management Script

USAGE:
    $0 <command>

COMMANDS:
    update          Update submodule, copy schema, and regenerate client
    update-schema   Update Git submodule and copy latest schema
    regenerate      Regenerate Python client from current schema
    status          Show current submodule and schema status
    help            Show this help message

SUBMODULE MANAGEMENT:
    The script uses a Git submodule (specs/mastodon-openapi) that tracks
    the abraham/mastodon-openapi repository, which is automatically updated
    weekly with the latest Mastodon API changes.

EXAMPLES:
    $0 update           # Full update: submodule + schema + client
    $0 update-schema    # Just update the schema from submodule
    $0 status           # Check current versions and status
EOF
}

check_dependencies() {
    local missing_deps=()
    
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    if ! command -v openapi-python-client &> /dev/null; then
        missing_deps+=("openapi-python-client")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Install with: pip install openapi-python-client"
        exit 1
    fi
}

init_submodule() {
    log_info "Initializing Git submodule..."
    
    cd "$PROJECT_ROOT"
    
    if [ ! -f "$SUBMODULE_PATH/.git" ]; then
        log_warning "Submodule not initialized. Adding mastodon-openapi submodule..."
        git submodule add https://github.com/abraham/mastodon-openapi.git specs/mastodon-openapi
    fi
    
    # Initialize and update submodule
    git submodule update --init --recursive
    log_success "Submodule initialized"
}

update_submodule() {
    log_info "Updating mastodon-openapi submodule..."
    
    cd "$PROJECT_ROOT"
    
    # Update submodule to latest commit
    git submodule update --remote specs/mastodon-openapi
    
    # Get current commit info
    cd "$SUBMODULE_PATH"
    local commit_hash=$(git rev-parse HEAD)
    local commit_date=$(git show -s --format=%ci HEAD)
    local commit_message=$(git show -s --format=%s HEAD)
    
    log_success "Submodule updated to: $commit_hash"
    log_info "Date: $commit_date"
    log_info "Message: $commit_message"
}

copy_schema() {
    log_info "Copying schema from submodule..."
    
    if [ ! -f "$SCHEMA_SOURCE" ]; then
        log_error "Schema not found at: $SCHEMA_SOURCE"
        log_info "Try building the submodule first: cd $SUBMODULE_PATH && npm install && npm run generate"
        exit 1
    fi
    
    # Create backup of existing schema
    if [ -f "$SCHEMA_DEST" ]; then
        cp "$SCHEMA_DEST" "${SCHEMA_DEST}.backup"
        log_info "Backed up existing schema to: ${SCHEMA_DEST}.backup"
    fi
    
    # Copy new schema
    cp "$SCHEMA_SOURCE" "$SCHEMA_DEST"
    
    # Show schema info
    local schema_size=$(du -h "$SCHEMA_DEST" | cut -f1)
    local schema_version=$(grep -o '"version": *"[^"]*"' "$SCHEMA_DEST" | head -1 | cut -d'"' -f4)
    
    log_success "Schema copied: $schema_size"
    log_info "API Version: $schema_version"
}

regenerate_client() {
    log_info "Regenerating Python client..."
    
    if [ ! -f "$SCHEMA_DEST" ]; then
        log_error "Schema not found at: $SCHEMA_DEST"
        log_info "Run '$0 update-schema' first"
        exit 1
    fi
    
    # Remove existing client
    if [ -d "$CLIENT_DIR" ]; then
        log_info "Removing existing client directory..."
        rm -rf "$CLIENT_DIR"
    fi
    
    # Generate new client
    cd "$PROJECT_ROOT"
    
    # Create config file to skip post-generation checks
    cat > openapi-python-client.yaml << EOF
post_gen_checks: false
EOF
    
    log_info "Generating new client (this may take a moment)..."
    if # Generate new Mastodon API client directly into the correct location
openapi-python-client generate --path specs/openapi.json --meta none --overwrite --output-path "$(dirname "$0")/../app/clients/mastodon" 2>&1 | tee /tmp/openapi-generate.log; then
        log_success "Client generated successfully at: $CLIENT_DIR"
    else
        log_error "Failed to generate client. Check /tmp/openapi-generate.log for details"
        exit 1
    fi
    
    # Clean up config file
    rm -f openapi-python-client.yaml
    
    # Show generation warnings/info
    if grep -q "WARNING" /tmp/openapi-generate.log; then
        log_warning "Some warnings occurred during generation:"
        grep "WARNING" /tmp/openapi-generate.log || true
    fi
}

show_status() {
    log_info "=== Mastodon API Client Status ==="
    
    # Submodule status
    if [ -d "$SUBMODULE_PATH" ]; then
        cd "$SUBMODULE_PATH"
        local commit_hash=$(git rev-parse HEAD)
        local commit_date=$(git show -s --format=%ci HEAD)
        echo "Submodule commit: $commit_hash"
        echo "Commit date: $commit_date"
        
        # Check if submodule is up to date
        git fetch origin main --quiet
        local remote_hash=$(git rev-parse origin/main)
        if [ "$commit_hash" = "$remote_hash" ]; then
            log_success "Submodule is up to date"
        else
            log_warning "Submodule is behind remote (run '$0 update-schema' to update)"
        fi
    else
        log_warning "Submodule not found"
    fi
    
    echo ""
    
    # Schema status
    if [ -f "$SCHEMA_DEST" ]; then
        local schema_size=$(du -h "$SCHEMA_DEST" | cut -f1)
        local schema_version=$(grep -o '"version": *"[^"]*"' "$SCHEMA_DEST" | head -1 | cut -d'"' -f4 || echo "unknown")
        local schema_date=$(stat -c %y "$SCHEMA_DEST" | cut -d' ' -f1)
        echo "Schema size: $schema_size"
        echo "Schema version: $schema_version" 
        echo "Schema date: $schema_date"
        log_success "Schema file exists"
    else
        log_warning "Schema file not found at: $SCHEMA_DEST"
    fi
    
    echo ""
    
    # Client status
    if [ -d "$CLIENT_DIR" ]; then
        local client_files=$(find "$CLIENT_DIR" -name "*.py" | wc -l)
        local client_date=$(stat -c %y "$CLIENT_DIR" | cut -d' ' -f1)
        echo "Client files: $client_files Python files"
        echo "Client generated: $client_date"
        log_success "Generated client exists"
    else
        log_warning "Generated client not found at: $CLIENT_DIR"
    fi
}

# Main command handling
case "${1:-help}" in
    "update")
        check_dependencies
        init_submodule
        update_submodule
        copy_schema
        regenerate_client
        log_success "Full update completed!"
        ;;
    "update-schema")
        check_dependencies
        init_submodule
        update_submodule
        copy_schema
        log_success "Schema update completed!"
        ;;
    "regenerate")
        check_dependencies
        regenerate_client
        log_success "Client regeneration completed!"
        ;;
    "status")
        show_status
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
