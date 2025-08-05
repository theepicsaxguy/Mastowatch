#!/bin/bash

# Enhanced Mastodon API Client Management Script
# Uses Git submodule for better version control and reproducibility
# NOTE: The generated client folder is fully purged before regeneration and marked as auto-generated.

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
    regenerate      Regenerate Python client from current schema (purges target folder first)
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

    # Add submodule only if it's not already tracked in .gitmodules
    if ! git config --file .gitmodules --get-regexp path 2>/dev/null | grep -q "specs/mastodon-openapi"; then
        log_warning "Submodule not found in .gitmodules. Adding mastodon-openapi submodule..."
        git submodule add https://github.com/abraham/mastodon-openapi.git specs/mastodon-openapi
    fi

    # Initialize and update submodule
    git submodule update --init --recursive "$SUBMODULE_PATH"
    log_success "Submodule initialized"
}

update_submodule() {
    log_info "Updating mastodon-openapi submodule..."

    cd "$PROJECT_ROOT"

    # Update submodule to latest commit
    git submodule update --remote specs/mastodon-openapi

    # Get current commit info
    cd "$SUBMODULE_PATH"
    local commit_hash
    commit_hash=$(git rev-parse HEAD)
    local commit_date
    commit_date=$(git show -s --format=%ci HEAD)
    local commit_message
    commit_message=$(git show -s --format=%s HEAD)

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

    # Copy new schema
    cp "$SCHEMA_SOURCE" "$SCHEMA_DEST"

    # Show schema info
    local schema_size
    schema_size=$(du -h "$SCHEMA_DEST" | cut -f1)
    local schema_version
    schema_version=$(grep -o '"version": *"[^"]*"' "$SCHEMA_DEST" | head -1 | cut -d'"' -f4 || echo "unknown")

    log_success "Schema copied: $schema_size"
    log_info "API Version: $schema_version"
}

purge_client_dir() {
    # Safety guard: refuse to purge suspicious paths
    case "$CLIENT_DIR" in
        "/"|"") log_error "Refusing to purge CLIENT_DIR because it resolves to '$CLIENT_DIR'"; exit 1 ;;
    esac
    if [[ "$CLIENT_DIR" != *"/app/clients/mastodon" ]]; then
        log_error "CLIENT_DIR does not look safe to purge: $CLIENT_DIR"
        exit 1
    fi

    mkdir -p "$CLIENT_DIR"
    log_info "Purging contents of client directory: $CLIENT_DIR"
    # Remove everything inside CLIENT_DIR (including hidden files) safely
    # shellcheck disable=SC2010
    if [ "$(ls -A "$CLIENT_DIR" 2>/dev/null | wc -l | tr -d ' ')" != "0" ]; then
        find "$CLIENT_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
    fi
}

write_autogen_notice() {
    cat > "$CLIENT_DIR/README.md" <<'EOF'
# Mastodon API Client (Auto-Generated)

**Do not edit files in this directory manually.**  
This folder is fully regenerated from the OpenAPI schema.

- Source schema: `specs/openapi.json`
- Regenerate using: `./scripts/THIS_SCRIPT.sh regenerate` (or `update`)
- Any manual changes here will be lost on the next generation.

EOF
    # Marker file that can be grepped by CI or tooling
    echo "AUTO-GENERATED. DO NOT EDIT." > "$CLIENT_DIR/.AUTOGENERATED"
}

regenerate_client() {
    log_info "Regenerating Python client..."

    if [ ! -f "$SCHEMA_DEST" ]; then
        log_error "Schema not found at: $SCHEMA_DEST"
        log_info "Run '$0 update-schema' first"
        exit 1
    fi

    purge_client_dir

    # Use a temp dir to avoid relying on undocumented output flags
    local TMPDIR
    TMPDIR=$(mktemp -d)
    log_info "Generating client in temp dir: $TMPDIR"

    # Create config file to skip post-generation checks
    cat > "$TMPDIR/openapi-python-client.yaml" << EOF
post_gen_checks: false
EOF

    pushd "$TMPDIR" >/dev/null

    log_info "Generating new client (this may take a moment)..."
    if openapi-python-client generate --path "$SCHEMA_DEST" --meta none --overwrite 2>&1 | tee /tmp/openapi-generate.log; then
        log_success "Client project generated"
    else
        log_error "Failed to generate client. Check /tmp/openapi-generate.log for details"
        popd >/dev/null || true
        rm -rf "$TMPDIR"
        exit 1
    fi

    # Locate the generated project root (the tool creates exactly one directory)
    local project_root
    project_root=$(find "$TMPDIR" -mindepth 1 -maxdepth 1 -type d | head -n 1 || true)
    if [ -z "${project_root:-}" ] || [ ! -d "$project_root" ]; then
        log_error "Could not locate generated project directory"
        popd >/dev/null || true
        rm -rf "$TMPDIR"
        exit 1
    fi

    # Locate the Python package dir inside the project (folder with __init__.py at top-level)
    local pkg_dir=""
    for d in "$project_root"/*; do
        if [ -d "$d" ] && [ -f "$d/__init__.py" ]; then
            pkg_dir="$d"
            break
        fi
    done
    # Fallback to common default
    if [ -z "$pkg_dir" ] && [ -d "$project_root/openapi_client" ]; then
        pkg_dir="$project_root/openapi_client"
    fi

    if [ -z "$pkg_dir" ]; then
        log_error "Failed to detect generated package directory"
        popd >/dev/null || true
        rm -rf "$TMPDIR"
        exit 1
    fi

    log_info "Detected generated package: $pkg_dir"

    # Copy package contents into CLIENT_DIR
    rsync -a --delete "$pkg_dir"/ "$CLIENT_DIR"/

    cat > "$CLIENT_DIR/__init__.py" <<'EOF'
"""Contains methods for accessing the API"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
EOF

    # Include typing marker if present
    if [ -f "$project_root/py.typed" ]; then
        cp "$project_root/py.typed" "$CLIENT_DIR/py.typed"
    fi

    popd >/dev/null

    # Write clear auto-generated notice
    write_autogen_notice

    # Clean up config/temp
    rm -rf "$TMPDIR"

    log_success "Client generated successfully at: $CLIENT_DIR"

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
        local commit_hash
        commit_hash=$(git rev-parse HEAD)
        local commit_date
        commit_date=$(git show -s --format=%ci HEAD)
        echo "Submodule commit: $commit_hash"
        echo "Commit date: $commit_date"

        # Check if submodule is up to date
        git fetch origin main --quiet || true
        local remote_hash
        remote_hash=$(git rev-parse origin/main 2>/dev/null || echo "")
        if [ -n "$remote_hash" ] && [ "$commit_hash" = "$remote_hash" ]; then
            log_success "Submodule is up to date"
        else
            log_warning "Submodule may be behind remote (run '$0 update-schema' to update)"
        fi
    else
        log_warning "Submodule not found"
    fi

    echo ""

    # Schema status
    if [ -f "$SCHEMA_DEST" ]; then
        local schema_size
        schema_size=$(du -h "$SCHEMA_DEST" | cut -f1)
        local schema_version
        schema_version=$(grep -o '"version": *"[^"]*"' "$SCHEMA_DEST" | head -1 | cut -d'"' -f4 || echo "unknown")
        # GNU stat format; may vary on macOS
        local schema_date
        schema_date=$(stat -c %y "$SCHEMA_DEST" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
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
        local client_files
        client_files=$(find "$CLIENT_DIR" -name "*.py" | wc -l | tr -d ' ')
        # GNU stat format; may vary on macOS
        local client_date
        client_date=$(stat -c %y "$CLIENT_DIR" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        echo "Client files: $client_files Python files"
        echo "Client generated: $client_date"
        if [ -f "$CLIENT_DIR/.AUTOGENERATED" ]; then
            log_success "Auto-generated marker present"
        fi
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
