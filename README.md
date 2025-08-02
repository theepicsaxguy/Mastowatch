# MastoWatch (Watch-and-Report Sidecar)

Analyze accounts/statuses and **file reports via API** so human moderators act in Mastodon's admin UI. **No auto-enforcement.**

## Quick start

To get a working stack, run:

```bash
docker compose up
```

If you want to develop locally, you can use the override file:

```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml up
```

Set these in `.env` (copied from `.env.example`):

* `INSTANCE_BASE`: your instance base URL
* `BOT_TOKEN`: token with `write:reports` scope
* `ADMIN_TOKEN`: token with admin read scopes
* `DRY_RUN`: `true` to log without sending reports
* `BATCH_SIZE`: admin polling batch size (default 80)

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


Endpoints:

* `GET /healthz`
* `GET /metrics`
* `POST /config/dry_run`  (body: `true|false`)
* `POST /dryrun/evaluate` (body: `{"account": {...}, "statuses": [...]}`)

## Notes

* Celery Beat schedules polling every 30 seconds.
* Alembic migrations run via the `migrate` service. Note that `alembic.ini` leaves `sqlalchemy.url` empty; the `DATABASE_URL` environment variable is used instead.
* Add Prometheus to scrape `/metrics` as desired.

```
