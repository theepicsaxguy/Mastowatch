# GitHub Copilot Instructions for MastoWatch

## Project Overview

MastoWatch is a **Mastodon moderation sidecar** that analyzes accounts/statuses and files reports via API for human moderators. It's a **watch-and-report system with no auto-enforcement** by default, built with FastAPI, Celery, PostgreSQL, and Redis.

## Architecture & Key Components

### Core Services Stack
- **API** (`app/api/`): FastAPI web server with routers for health checks, webhooks, and admin endpoints. `app/main.py` is the entrypoint.
- **Worker** (`app/tasks/jobs.py`): Celery workers for background account analysis and reporting
- **Beat**: Celery scheduler for periodic polling (every 30s)
- **Database**: PostgreSQL with Alembic migrations
- **Redis**: Celery broker and caching for deduplication and rate limiting

### Rule Engine & Analysis
- **Rules**: **Database-driven exclusively** (`app/services/rule_service.py`)
- **Scanning**: Enhanced scanning system with deduplication (`app/enhanced_scanning.py`)
- **Enforcement**: Optional automated actions (`app/services/enforcement_service.py`)
- **Detectors**: Pluggable detection modules (`app/services/detectors/`)

### Generated API Client Pattern
- **Auto-updating Mastodon client**: Uses OpenAPI spec from `abraham/mastodon-openapi` submodule
- **Client location**: `app/clients/mastodon/` (generated, do not edit manually)
- **Update script**: `scripts/update_mastodon_client.sh` for syncing with upstream API
- **Type safety**: Full Python typing with Pydantic models for all Mastodon API interactions

## Development Workflows

### Docker Compose Commands
```bash
# Development with hot reload
make dev  # or docker compose -f docker-compose.yml -f docker-compose.override.yml up

# Backend only (for frontend dev)
make backend-only

# Production
make prod
```

### Testing Strategy
- **Comprehensive test suite**: 22 test scenarios covering edge cases
- **Environment isolation**: Uses test database and Redis instances
- **Mock external APIs**: Mastodon API calls are mocked in tests
- **Run tests**: `make test` or `python -m unittest discover tests`

### Code Quality Tools
- **Formatting**: Black with 127-char line length (`make format`)
- **Linting**: Ruff with custom rules banning direct HTTP libraries (`make lint`)
- **Type checking**: MyPy with selective strictness (`make typecheck`)
- **HTTP library policy**: Use generated Mastodon client only, no direct `requests`/`httpx`

### Database Operations
```bash
# Run migrations
make migration

# Generate new migration
make new-migration name="description"

# Database shell
make shell-db
```

## Critical Configuration Patterns

### Environment Variables Structure
- **Required**: `INSTANCE_BASE`, `BOT_TOKEN`, `ADMIN_TOKEN`, `API_KEY`, `WEBHOOK_SECRET`
- **OAuth for admin UI**: `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `OAUTH_REDIRECT_URI`
- **Safety controls**: `DRY_RUN=true`, `PANIC_STOP=false`, `SKIP_STARTUP_VALIDATION=false`
- **Database URL format**: `postgresql+psycopg://user:pass@host:port/db`

### API Authentication Patterns
- **Webhook validation**: HMAC SHA256 signature verification
- **Admin UI Auth**: OAuth2 flow with secure, HttpOnly session cookies for all moderator interactions with the frontend
- **Programmatic API Auth**: A static API key (`X-API-Key` header) for server-to-server calls or scripts
- **Rate limiting**: Handled by a **dedicated service** that wraps generated client calls

### Task Queue Architecture
- **Polling tasks**: `poll_admin_accounts` (remote), `poll_admin_accounts_local`
- **Event processing**: `process_new_report`, `process_new_status` (webhook-driven)
- **Analysis pipeline**: `analyze_and_maybe_report` with rule evaluation
- **Cursor management**: PostgreSQL-based pagination for account polling

## Project-Specific Conventions

### Data Flow Patterns
1. **Account Discovery**: Celery Beat → polling tasks → account persistence
2. **Rule Evaluation**: Account + statuses → rule engine → score calculation
3. **Report Generation**: Score threshold → dedupe check → Mastodon API submission
4. **Webhook Processing**: Real-time events → task queue → analysis pipeline

### Error Handling Standards
- **Structured logging**: JSON format with request IDs for tracing
- **Health checks**: `/healthz` returns 503 for service unavailability
- **Graceful degradation**: `PANIC_STOP` halts processing, `DRY_RUN` logs without action
- **Retry strategies**: Exponential backoff with jitter for external API calls

### Database Schema Patterns
- **Foreign keys**: Enforce referential integrity across all tables
- **UPSERT patterns**: Use PostgreSQL `ON CONFLICT DO UPDATE` for idempotent operations
- **Deduplication**: `dedupe_key` fields prevent duplicate reports
- **Timestamps**: All tables have `created_at`/`updated_at` with timezone

### Frontend Integration
- **Static assets**: Mounted at `/dashboard` (built separately)
- **OAuth popup flow**: Admin login with `postMessage` to parent window
- **Real-time updates**: WebSocket or polling for configuration changes
- **CORS configuration**: `CORS_ORIGINS` for development environments

## File Structure Patterns

### Key Directories
- `app/api/`: FastAPI routers (analytics, auth, config, rules, scanning)
- `app/services/`: Business logic (rule service, enforcement, detectors)
- `app/tasks/`: Celery job definitions and queue management
- `app/clients/mastodon/`: Generated API client (auto-updated)
- `tests/`: Comprehensive test suite with environment isolation
- `specs/`: OpenAPI schemas and submodule for upstream sync

### Configuration Files
- `pyproject.toml`: Black, MyPy, Ruff configuration with custom rules
- `alembic.ini`: Database migration config (uses `DATABASE_URL` env var)
- `docker-compose.yml`: Production stack definition
- `docker-compose.override.yml`: Development overrides with hot reload

When working on this codebase, always consider the moderation context - this system handles sensitive content and must be reliable, auditable, and safe.
