#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
# Get directories relative to the script's location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"
SUBMODULE_PATH="$PROJECT_ROOT/specs/mastodon-openapi"
SCHEMA_IN="$SUBMODULE_PATH/dist/schema.json"
SCHEMA_OUT="$SUBMODULE_PATH/dist/schema.cleaned.json"
CLIENT_DIR="$PROJECT_ROOT/backend/app/clients/mastodon"

# --- Logging helpers ---
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log() { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()  { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $*"; }
err() { echo -e "${RED}[ERROR]${NC} $*" >&2; } # Errors to stderr

# --- Prerequisite Checks ---
check_deps() {
  log "Checking for dependencies..."
  local miss=()
  command -v git >/dev/null || miss+=("git")
  command -v node >/dev/null || miss+=("node")
  command -v npm >/dev/null || miss+=("npm")
  command -v openapi-python-client >/dev/null || miss+=("openapi-python-client")
  
  if [ ${#miss[@]} -gt 0 ]; then
    err "Missing dependencies: ${miss[*]}. Please install them."
    exit 1
  fi
  ok "All dependencies are present."
}

# --- Git Submodule Management ---
init_submodule() {
  if [ ! -d "$SUBMODULE_PATH/.git" ]; then
    log "Initializing mastodon-openapi submodule..."
    cd "$PROJECT_ROOT"
    git submodule add https://github.com/abraham/mastodon-openapi.git specs/mastodon-openapi
    git submodule update --init --recursive
    ok "Submodule initialized."
  else
    log "Submodule already initialized."
  fi
}

update_submodule() {
  log "Updating submodule to the latest commit..."
  cd "$SUBMODULE_PATH"
  git fetch
  git checkout main # Or the branch you prefer
  git pull
  cd "$PROJECT_ROOT"
  git add "$SUBMODULE_PATH" # Stage the new submodule commit
  ok "Submodule updated to $(git -C "$SUBMODULE_PATH" rev-parse --short HEAD)."
}

# --- Schema Processing ---
sanitize_schema() {
  log "Sanitizing OpenAPI schema..."
  [ -f "$SCHEMA_IN" ] || { err "Input schema not found: $SCHEMA_IN"; exit 1; }
  
  # Run the enhanced sanitizer script
  node "$PROJECT_ROOT/scripts/sanitize_openapi.mjs" "$SCHEMA_IN" "$SCHEMA_OUT"
  
  ok "Schema sanitized successfully: $SCHEMA_OUT"
}

# --- Client Generation ---
regenerate_client() {
  log "Regenerating Python client with temporary ruff override..."
  
  # Clean the target directory before generating.
  mkdir -p "$CLIENT_DIR"
  find "$CLIENT_DIR" -mindepth 1 -maxdepth 1 -not -name '__init__.py' -exec rm -rf {} +

  # Temporarily hide pyproject.toml to avoid strict ruff rules during generation
  cd "$PROJECT_ROOT"
  if [ -f "pyproject.toml" ]; then
    mv "pyproject.toml" "pyproject.toml.backup"
  fi

  # Generate client with minimal configuration to avoid conflicts
  if openapi-python-client generate \
    --path "$SCHEMA_OUT" \
    --output-path "$CLIENT_DIR" \
    --meta none \
    --overwrite \
    --no-fail-on-warning \
    2>&1 | tee /tmp/openapi-gen.log; then
    
    # Restore pyproject.toml
    if [ -f "pyproject.toml.backup" ]; then
      mv "pyproject.toml.backup" "pyproject.toml"
    fi
    
    # Check for actual generation failures vs. linting issues
    if grep -q "Failed to generate" /tmp/openapi-gen.log; then
      err "Client generation failed. See /tmp/openapi-gen.log for details."
      exit 1
    fi
    
    ok "Python client regenerated at: $CLIENT_DIR"
  else
    # Restore pyproject.toml even on failure
    if [ -f "pyproject.toml.backup" ]; then
      mv "pyproject.toml.backup" "pyproject.toml"
    fi
    err "Client generation failed catastrophically. See /tmp/openapi-gen.log for the full error."
    exit 1
  fi
}

# --- Status reporting ---
show_status() {
  log "Current API client status:"
  echo "Submodule HEAD: $(git -C "$SUBMODULE_PATH" rev-parse --short HEAD 2>/dev/null || echo 'n/a')"
  echo "Schema (input):   $([ -f "$SCHEMA_IN" ] && echo 'present' || echo 'missing')"
  echo "Schema (cleaned): $([ -f "$SCHEMA_OUT" ] && echo 'present' || echo 'missing')"
  echo "Client files:     $(find "$CLIENT_DIR" -name '*.py' 2>/dev/null | wc -l | tr -d ' ') Python files"
  if [ -f "$CLIENT_DIR/client.py" ]; then
    echo "Main client:      present"
  else
    echo "Main client:      missing"
  fi
}

# --- Main script logic ---
main() {
  check_deps
  init_submodule
  update_submodule
  sanitize_schema
  regenerate_client
  ok "Client generation process completed successfully."
}

# --- Command-line argument handling ---
case "${1:-update}" in
  update)
    main
    ;;
  regenerate)
    check_deps
    sanitize_schema
    regenerate_client
    ;;
  status)
    show_status
    ;;
  *)
    err "Unknown command: '$1'. Use 'update', 'regenerate', or 'status'."
    exit 1
    ;;
esac
