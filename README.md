# MastoWatch (Watch-and-Report Sidecar)

Analyze accounts/statuses and **file reports via API** so human moderators act in Mastodon's admin UI. **No auto-enforcement.**

## Quick start

```bash
docker compose build
docker compose up -d db redis
# wait until db is healthy
docker compose run --rm migrate
docker compose up -d api worker beat
````

Set these in `docker-compose.yml`:

* `MST_BASE_URL`: your instance base URL
* `BOT_TOKEN`: token with `write:reports`
* `ADMIN_TOKEN`: token with the minimal admin read scopes you use
* `DRY_RUN`: `true` to log without sending reports
* `BATCH_SIZE`: admin polling batch size (default 80)

Endpoints:

* `GET /healthz`
* `GET /metrics`
* `POST /config/dry_run`  (body: `true|false`)
* `POST /dryrun/evaluate` (body: `{"account": {...}, "statuses": [...]}`)

## Notes

* Celery Beat schedules polling every 30 seconds.
* Alembic migrations run via the `migrate` service.
* Add Prometheus to scrape `/metrics` as desired.

```
