# MastoWatch (Watch-and-Report Sidecar)

Analyze accounts/statuses and **file reports via API** so human moderators act in Mastodon's admin UI. **No auto-enforcement.**

## Production-Ready Features

- ✅ **Enhanced Error Handling**: Comprehensive API error responses with structured logging and request IDs
- ✅ **Health Checks**: Robust health monitoring with proper HTTP status codes (503 for service unavailability)
- ✅ **Security**: Webhook signature validation, API key authentication, and security scanning
- ✅ **Database**: Foreign keys, performance indexes, reliable migrations
- ✅ **Monitoring**: Prometheus metrics, structured JSON logging, and detailed analytics
- ✅ **Frontend**: Enhanced settings interface with error states and real-time configuration
- ✅ **Testing**: Comprehensive edge case test coverage (22 test scenarios)
- ✅ **CI/CD**: Automated testing, static analysis, and code formatting
- ✅ **Audit Logs**: Enforcement actions recorded with rule context and API responses
- ✅ **User Notifications**: Warnings and suspensions include messages sent through Mastodon

## Quick start

To get a working stack, run:

```bash
docker compose up
```

If you want to develop locally, you can use the override file:

```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml up
```

## Configuration

Set these in `.env` (copied from `.env.example`):

### Required Settings
* `INSTANCE_BASE`: your instance base URL
* `BOT_TOKEN`: token with `write:reports` scope
* `ADMIN_TOKEN`: token with admin read scopes
* `API_KEY`: random string for API authentication
* `WEBHOOK_SECRET`: random string for webhook signature validation

### OAuth Admin Login (Required for Web UI)
* `OAUTH_CLIENT_ID`: OAuth application client ID
* `OAUTH_CLIENT_SECRET`: OAuth application client secret
* `OAUTH_REDIRECT_URI`: OAuth callback URL (e.g., `https://your.instance/admin/callback`)
* `OAUTH_SCOPE`: OAuth scopes for admin login (default: `read:accounts`)
* `SESSION_SECRET_KEY`: Random secret for session cookies

### Optional Settings
* `DRY_RUN`: `true` to log without sending reports (default: `false`)
* `PANIC_STOP`: `true` to halt all processing (default: `false`)
* `MAX_PAGES_PER_POLL`: admin polling pages per batch (default: 3)
* `USER_AGENT`: user agent for Mastodon requests (default: `MastoWatch/<VERSION> (+moderation-sidecar)`)
* `HTTP_TIMEOUT`: seconds before Mastodon requests time out (default: `30`)
* `VERSION`: application version (default: `0.1.0`)
* `SKIP_STARTUP_VALIDATION`: `true` to skip startup checks (for testing only)
* `UI_ORIGIN`: origin for the dashboard UI
* `MIN_MASTODON_VERSION`: minimum supported Mastodon version (default: `4.0.0`)
* `POLL_ADMIN_ACCOUNTS_INTERVAL`: seconds between remote admin polls (default: `30`)
* `POLL_ADMIN_ACCOUNTS_LOCAL_INTERVAL`: seconds between local admin polls (default: `30`)
* `QUEUE_STATS_INTERVAL`: seconds between queue metrics snapshots (default: `15`)
* `VITE_API_URL`: API base URL for the frontend

### Getting Mastodon Access Tokens

This application uses **direct access tokens** rather than OAuth2 client credentials. You need to create two applications in your Mastodon instance:

#### 1. Admin Token (for moderation operations)
1. Go to your Mastodon instance → **Settings → Development**
2. Click **"New Application"**
3. Configure:
   - **Application name**: `MastoWatch Admin`
   - **Scopes**: Select `admin:read` and `admin:write`
4. Click **"Submit"**
5. Copy the **"Your access token"** → use as `ADMIN_TOKEN` in `.env`

#### 2. Bot Token (for reading and reporting)
1. Create another new application
2. Configure:
   - **Application name**: `MastoWatch Bot`  
   - **Scopes**: Select `read` and `write:reports`
3. Click **"Submit"**
4. Copy the **"Your access token"** → use as `BOT_TOKEN` in `.env`

**Note**: You only need the access tokens, not the client key/secret shown in the application details.

#### 3. OAuth Application (for admin web interface)
1. Create a third application for OAuth login
2. Configure:
   - **Application name**: `MastoWatch OAuth`
   - **Scopes**: Select `read:accounts` (for user verification)
   - **Redirect URI**: Your callback URL (e.g., `https://your.domain/admin/callback`)
3. Click **"Submit"**
4. Copy the **"Client key"** → use as `OAUTH_CLIENT_ID` in `.env`
5. Copy the **"Client secret"** → use as `OAUTH_CLIENT_SECRET` in `.env`

## API Client

MastoWatch uses a **type-safe, auto-updating Mastodon API client** based on the community-maintained OpenAPI specification:

- **Automatic updates**: Weekly sync with [abraham/mastodon-openapi](https://github.com/abraham/mastodon-openapi)
- **Type safety**: Generated Python client with full IDE support and validation
- **Backward compatibility**: Fallback to raw HTTP for admin endpoints
- **Documentation**: Self-documenting through types

### Managing the API Client

```bash
# Check current status
make api-client-status

# Update from latest Mastodon API spec
make update-mastodon-client

# Just update the schema
make update-api-spec

# Just regenerate client
make regenerate-client
```

See [docs/mastodon-api-client.md](docs/mastodon-api-client.md) for detailed documentation.

Endpoints:

### API Endpoints

#### Health & Monitoring
* `GET /healthz` - Health check with service status (returns 503 if services unavailable)
* `GET /metrics` - Prometheus metrics for monitoring

#### Configuration Management (requires admin login)
* `GET /config` - Return non-sensitive configuration details
* `POST /config/dry_run?enable=true|false` - Toggle dry run mode
* `POST /config/panic_stop?enable=true|false` - Emergency stop all processing

#### Rule Management (requires admin login)
* `GET /rules` - List all rules
* `POST /rules` - Create a rule
* `PUT /rules/{id}` - Update a rule
* `DELETE /rules/{id}` - Delete a rule
* `POST /rules/{id}/toggle` - Enable or disable a rule

#### Analytics & Data (requires admin login)
* `GET /analytics/overview` - System analytics overview with account/report metrics
* `GET /analytics/timeline?days=N` - Timeline analytics for the past N days (1-365)
* `GET /logs` - Enforcement audit log entries

#### Authentication
* `GET /admin/login` - Initiate OAuth login flow for admin access
* `GET /admin/callback` - OAuth callback handler
* `POST /admin/logout` - Clear admin session
* `GET /api/v1/me` - Get current user information

#### Testing & Validation  
* `POST /dryrun/evaluate` - Test rule evaluation (body: `{"account": {...}, "statuses": [...]}`) returns `{"score": float, "hits": [[rule, weight, evidence], ...]}`

#### Webhooks
* `POST /webhooks/status` - Webhook endpoint for Mastodon status updates (requires signature validation)

### Error Handling
All API endpoints return structured error responses with:
- **Request IDs** for tracing and debugging
- **Detailed error messages** with context
- **Proper HTTP status codes** (400/401/404/422/500/503)
- **Structured logging** with JSON format for monitoring

## Notes

* Celery Beat intervals are configurable via environment variables.
* All endpoints use structured JSON logging with request IDs for troubleshooting.
* Alembic migrations run via the `migrate` service. Note that `alembic.ini` leaves `sqlalchemy.url` empty; the `DATABASE_URL` environment variable is used instead.
* Add Prometheus to scrape `/metrics` as desired.
* Foreign keys ensure data integrity; performance indexes optimize common queries.

## Legal Notice

Every page shows a footer linking to [goingadark.social](https://goingadark.social). The app refuses to run without it. Don't remove or rename this credit; it's part of the license.
