# GitHub Copilot Instructions for MastoWatch

## Project Overview

MastoWatch is a **Mastodon moderation sidecar** that analyzes accounts/statuses and files reports via API for human moderators. It's a **watch-and-report system with no auto-enforcement** by default, built with FastAPI, Celery, PostgreSQL, and Redis.

## Architecture & Key Components

### Core Services Stack
- **API** (`app/api/`): FastAPI web server with routers for analytics, auth, config, rules, and scanning. `app/main.py` is the entrypoint.
- **Worker** (`app/tasks/jobs.py`): Celery workers for background account analysis and webhook event processing.
- **Beat**: Celery scheduler for periodic polling (every 30s).
- **Database**: PostgreSQL with Alembic for migrations.
- **Redis**: Celery broker and caching for deduplication and rate limiting.

### Rule Engine & Analysis
- **Rules**: **Database-driven exclusively** via the `RuleService` (`app/services/rule_service.py`). The old `rules.yml` is deprecated and no longer used.
- **Scanning**: An enhanced scanning system (`app/enhanced_scanning.py`) handles efficient, deduplicated account scanning.
- **Enforcement**: Optional automated actions are managed by the `EnforcementService` (`app/services/enforcement_service.py`).
- **Detectors**: Pluggable detection modules (`app/services/detectors/`) implement specific logic (regex, keyword, behavioral) for the rule engine.

### Mastodon API Client Wrapper
- **Primary Interface**: All application logic **must** interact with the Mastodon API through the `MastoClient` wrapper class in `app/mastodon_client.py`. This class handles rate-limiting, metrics, and provides a simplified, high-level interface.
- **Generated Client**: The `MastoClient` internally uses an **auto-generated, type-safe client** located in `app/clients/mastodon/`. This generated code should **never be called directly** from other parts of the application.
- **Update Script**: The generated client is kept in sync with the upstream Mastodon API specification using `scripts/update_mastodon_client.sh`.

## Development Workflows

### Make Commands (Preferred)
**ALWAYS use `make` commands when working with this project.** The project includes a comprehensive Makefile that provides convenient shortcuts for all common development tasks.

```bash
# Development with hot reload
make dev

# Backend only (for frontend development)
make backend-only

# Production environment
make prod

# Stop all services
make stop

# Clean up containers and volumes
make clean

# View service status
make status

# View logs
make logs              # All services
make logs-api          # API only
make logs-worker       # Worker only
make logs-frontend     # Frontend only
```

### Testing Strategy
- **Restructured Test Suite**: Tests are organized by feature area, mirroring the application structure (`tests/api`, `tests/services`, `tests/tasks`).
- **Isolation**: Tests use an in-memory SQLite database and a separate Redis instance to ensure isolation and prevent side effects.
- **Mocking External APIs**: All outbound calls to the Mastodon API are mocked using `unittest.mock.patch` to prevent real network requests during tests.
- **Run tests**: `make test`

### Code Quality Tools
- **Formatting**: Black with a **120-character** line length (`make format`).
- **Format checking**: `make format-check` to verify formatting without making changes.
- **Linting**: Ruff with custom rules in `pyproject.toml` to ban direct use of `requests` and `httpx` (`make lint`).
- **Type checking**: MyPy with selective strictness (`make typecheck`).
- **All quality checks**: `make check` runs lint, format-check, typecheck, and test in sequence.
- **HTTP Library Policy**: Only the `MastoClient` wrapper is permitted to interact with the Mastodon API. Direct use of `requests` or `httpx` elsewhere is a linting error.

### Database Operations
```bash
# Run migrations (automatic during startup)
make migration name="your_migration_description"

# Database shell
make shell-db
```

### Service Management
```bash
# Restart specific services
make restart-api
make restart-worker  
make restart-frontend

# Enter container shells
make shell-api       # API container shell
```

### Mastodon Client Management
```bash
# Update OpenAPI spec from submodule
make update-api-spec

# Regenerate typed client from current spec  
make regenerate-client

# Full update: submodule + spec + client
make update-mastodon-client

# Show current API client status
make api-client-status
```

## Critical Configuration Patterns

### Environment Variables Structure
- **Required**: `INSTANCE_BASE`, `BOT_TOKEN`, `ADMIN_TOKEN`, `API_KEY`, `WEBHOOK_SECRET`
- **OAuth for admin UI**: `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `OAUTH_REDIRECT_URI`
- **Safety controls**: `DRY_RUN=true`, `PANIC_STOP=false`, `SKIP_STARTUP_VALIDATION=false`
- **Database URL format**: `postgresql+psycopg://user:pass@host:port/db`

### API Authentication Patterns
- **Webhook Validation**: Inbound webhooks are validated using an HMAC SHA256 signature in the `X-Hub-Signature-256` header.
- **Admin UI Auth**: An OAuth2 flow provides a secure, HttpOnly session cookie for all moderator interactions with the frontend.
- **Programmatic API Auth**: A static API key is required in the `X-API-Key` header for server-to-server calls or scripts.
- **Rate Limiting**: Handled centrally by the `MastoClient` wrapper, which respects Mastodon's rate-limit headers.

### Task Queue Architecture
- **Polling Tasks**: `poll_admin_accounts` (remote) and `poll_admin_accounts_local` for discovering accounts.
- **Event Processing**: `process_new_report` and `process_new_status` are triggered by `report.created` and `status.created` webhook events, respectively.
- **Analysis Pipeline**: The `analyze_and_maybe_report` task evaluates accounts against the database rules and triggers enforcement actions.
- **Cursor Management**: PostgreSQL-based cursors are used for paginating through accounts during polling tasks.

## Project-Specific Conventions

### Data Flow Patterns
1.  **Account Discovery**: Celery Beat → `poll_admin_accounts` → Account persistence in PostgreSQL.
2.  **Rule Evaluation**: An account and its statuses are passed to the `RuleService`, which uses various detectors to find violations.
3.  **Report Generation/Enforcement**: If a violation's score exceeds the rule's `trigger_threshold`, the `EnforcementService` is called to perform an action (e.g., file a report) via the `MastoClient`.
4.  **Webhook Processing**: A real-time event from Mastodon (e.g., `status.created`) hits the webhook endpoint, which enqueues a specific Celery task (`process_new_status`) for immediate analysis.

### Error Handling Standards
- **Structured Logging**: JSON format with request IDs for easy tracing in production.
- **Health Checks**: The `/healthz` endpoint returns a `503` status if the database or Redis is unavailable.
- **Graceful Degradation**: `PANIC_STOP` halts all background processing. `DRY_RUN` logs intended actions without executing them.
- **Retry Strategies**: Celery tasks use exponential backoff with jitter for retrying on failure.

### Database Schema Patterns
- **Foreign Keys**: Enforce referential integrity across all tables.
- **UPSERT Patterns**: Use PostgreSQL's `ON CONFLICT DO UPDATE` for idempotent operations, such as updating account data.
- **Deduplication**: `dedupe_key` fields prevent the system from filing duplicate reports for the same underlying issue.
- **Timestamps**: All tables include `created_at` and `updated_at` with timezone information.

### Frontend Integration
- **Static Assets**: Mounted at `/dashboard` (built separately).
- **OAuth Popup Flow**: Admin login uses a popup window that communicates success or failure to the parent window via `postMessage`.
- **CORS Configuration**: Controlled by the `CORS_ORIGINS` environment variable.

## File Structure Patterns

### Key Directories
- `app/api/`: FastAPI routers, organized by resource (analytics, auth, rules, etc.).
- `app/services/`: Core business logic (RuleService, EnforcementService, Detectors).
- `app/tasks/`: Celery job definitions.
- `app/clients/mastodon/`: **Auto-generated** Mastodon API client. **Do not edit manually.**
- `tests/`: Test suite, structured to mirror the application layout.
- `specs/`: OpenAPI schemas for client generation.

### Configuration Files
- `pyproject.toml`: Black, MyPy, and Ruff configurations, including custom rules to ban direct HTTP library usage.
- `alembic.ini`: Database migration settings (uses the `DATABASE_URL` environment variable).
- `docker-compose.yml`: Production stack definition.
- `docker-compose.override.yml`: Development overrides with hot-reloading.

When working on this codebase, always consider the moderation context. This system handles sensitive content and must be reliable, auditable, and safe.
