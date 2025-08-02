#!/bin/bash

# Check for direct httpx usage outside /app/clients and other allowed locations
# This helps ensure we use the generated client properly

set -e

ALLOWED_DIRS=(
    "app/clients"
    "tests"
    "scripts"
)

# Files with direct httpx imports that are exceptions to the rule
ALLOWED_FILES=(
    "app/oauth.py"  # Uses httpx for OAuth flows with generated client session
    "app/mastodon_client.py"  # DEPRECATED - allowed until fully migrated
)

echo "Checking for direct httpx usage..."

# Find all Python files
PYTHON_FILES=$(find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./__pycache__/*" -not -path "./.git/*")

VIOLATIONS=()

for file in $PYTHON_FILES; do
    # Skip allowed directories
    skip_file=false
    for allowed_dir in "${ALLOWED_DIRS[@]}"; do
        if [[ $file == ./$allowed_dir/* ]]; then
            skip_file=true
            break
        fi
    done
    
    # Skip allowed specific files
    for allowed_file in "${ALLOWED_FILES[@]}"; do
        if [[ $file == ./$allowed_file ]]; then
            skip_file=true
            break
        fi
    done
    
    if [[ $skip_file == true ]]; then
        continue
    fi
    
    # Check for direct httpx usage
    if grep -q "import httpx\|from httpx" "$file"; then
        # Allow httpx usage if it's through the generated client session
        if ! grep -q "get_async_httpx_client\|get_httpx_client" "$file"; then
            VIOLATIONS+=("$file")
        fi
    fi
done

if [[ ${#VIOLATIONS[@]} -eq 0 ]]; then
    echo "✅ No direct httpx usage violations found"
    exit 0
else
    echo "❌ Found direct httpx usage in the following files:"
    for violation in "${VIOLATIONS[@]}"; do
        echo "  - $violation"
        echo "    Lines with httpx:"
        grep -n "import httpx\|from httpx" "$violation" || true
    done
    echo ""
    echo "Please use the generated client's HTTP session instead:"
    echo "  async with client.get_async_httpx_client() as http_client:"
    echo "      response = await http_client.get(...)"
    echo ""
    echo "Or add the file to ALLOWED_FILES in this script if it's a legitimate exception."
    exit 1
fi
