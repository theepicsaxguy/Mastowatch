#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SUBMODULE_PATH="$PROJECT_ROOT/specs/mastodon-openapi"
SCHEMA_IN="$SUBMODULE_PATH/dist/schema.json"
SCHEMA_OUT="$SUBMODULE_PATH/dist/schema.cleaned.json"
CLIENT_DIR="$PROJECT_ROOT/backend/app/clients/mastodon"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log() { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()  { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $*"; }
err() { echo -e "${RED}[ERROR]${NC} $*"; }

check_deps() {
  local miss=()
  command -v git >/dev/null || miss+=("git")
  command -v node >/dev/null || miss+=("node")
  command -v npm  >/dev/null || miss+=("npm")
  command -v openapi-python-client >/dev/null || miss+=("openapi-python-client")
  if [ ${#miss[@]} -gt 0 ]; then err "Missing: ${miss[*]}"; exit 1; fi
}

init_submodule() {
  log "Initializing mastodon-openapi submodule..."
  cd "$PROJECT_ROOT"
  if ! git config --file .gitmodules --get-regexp path 2>/dev/null | grep -q "specs/mastodon-openapi"; then
    git submodule add https://github.com/abraham/mastodon-openapi.git specs/mastodon-openapi
  fi
  git submodule update --init specs/mastodon-openapi
  ok "Submodule initialized"
}

update_submodule() {
  log "Updating submodule to latest committed schema..."
  cd "$PROJECT_ROOT"
  git submodule update --remote specs/mastodon-openapi
  ok "Submodule at $(cd "$SUBMODULE_PATH" && git rev-parse --short HEAD)"
}

ensure_node_deps() {
  # Install sanitizer deps once; use ci if lock exists, else install to create it.
  cd "$PROJECT_ROOT"
  if [ -f package.json ]; then
    if [ -f package-lock.json ]; then
      log "Installing Node deps (npm ci)…"
      npm ci --no-audit --no-fund
    else
      log "No package-lock.json found; running npm install once to create it…"
      npm install --no-audit --no-fund
    fi
  else
    err "package.json missing at repo root; add it (see provided package.json)"; exit 1
  fi
}

sanitize_schema() {
  log "Sanitizing schema via OpenAPI 3.1 meta-schema (endpoint-agnostic)…"
  [ -f "$SCHEMA_IN" ] || { err "Schema not found: $SCHEMA_IN"; exit 1; }

  # Ensure sanitizer deps exist INSIDE the submodule without touching package.json/lock
  cd "$SUBMODULE_PATH"
  NEED_INSTALL=0
  [ ! -d "node_modules/@apidevtools/openapi-schemas" ] && NEED_INSTALL=1
  [ ! -d "node_modules/ajv" ] && NEED_INSTALL=1
  [ ! -d "node_modules/ajv-formats" ] && NEED_INSTALL=1
  if [ "$NEED_INSTALL" -eq 1 ]; then
    log "Installing sanitizer deps in submodule/node_modules (no-save, no lock, no scripts)…"
    npm install --no-save --no-package-lock --ignore-scripts \
    ajv@^8 ajv-formats@^3 @apidevtools/openapi-schemas@latest
  fi

  # Run sanitizer with module resolution from the submodule
  NODE_PATH="$SUBMODULE_PATH/node_modules" \
    node "$PROJECT_ROOT/scripts/sanitize_openapi.mjs" "$SCHEMA_IN" "$SCHEMA_OUT"

  ok "Cleaned schema: $SCHEMA_OUT"
}


regenerate_client() {
  log "Regenerating Python client…"
  mkdir -p "$CLIENT_DIR"
  find "$CLIENT_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} + || true

  local TMPDIR; TMPDIR="$(mktemp -d)"
  log "Using temp dir: $TMPDIR"
  cat > "$TMPDIR/openapi-python-client.yaml" <<EOF
post_gen_checks: false
EOF

  if openapi-python-client generate --path "$SCHEMA_OUT" --meta none --overwrite --output-path "$TMPDIR" 2>&1 | tee /tmp/openapi-gen.log; then :; else
    err "Client generation failed; see /tmp/openapi-gen.log"; rm -rf "$TMPDIR"; exit 1
  fi

  local PKG; PKG="$(find "$TMPDIR" -mindepth 1 -maxdepth 1 -type d | head -n1)"
  [ -n "$PKG" ] || { err "No generated package found"; rm -rf "$TMPDIR"; exit 1; }

  rsync -a --delete "$PKG"/ "$CLIENT_DIR"/
  cat > "$CLIENT_DIR/__init__.py" <<'PY'
"""Auto-generated Mastodon client"""
from .client import AuthenticatedClient, Client
__all__ = ("AuthenticatedClient", "Client")
PY

  [ -f "$PKG/py.typed" ] && cp "$PKG/py.typed" "$CLIENT_DIR/py.typed"
  rm -rf "$TMPDIR"
  ok "Client generated at: $CLIENT_DIR"
  if grep -q "WARNING" /tmp/openapi-gen.log; then
    warn "Generator warnings detected (non-fatal). See /tmp/openapi-gen.log"
  fi
}

show_status() {
  echo "Submodule HEAD: $(cd "$SUBMODULE_PATH" && git rev-parse --short HEAD 2>/dev/null || echo 'n/a')"
  echo "Schema (in):  $([ -f "$SCHEMA_IN" ] && echo 'present' || echo 'missing')"
  echo "Schema (out): $([ -f "$SCHEMA_OUT" ] && echo 'present' || echo 'missing')"
  echo "Client files:  $(find "$CLIENT_DIR" -name '*.py' 2>/dev/null | wc -l | tr -d ' ')"
}

case "${1:-update}" in
  update)      check_deps; init_submodule; update_submodule; sanitize_schema; regenerate_client ;;
  regenerate)  check_deps; sanitize_schema; regenerate_client ;;
  status)      show_status ;;
  help|-h|--help) echo "Usage: $0 [update|regenerate|status]";;
  *) err "Unknown command: $1"; exit 1;;
esac
