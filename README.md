# MastoWatch (Watch-and-Report Sidecar)

Analyze accounts/statuses and **file reports via API** so human moderators act in Mastodon's admin UI. **No auto-enforcement.**

## Quick start

To get a working stack, follow these steps:

### 1) Host "dev-doctor" (one-time fix)

Run the `scripts/dev-doctor.sh` script to ensure your host is set up correctly for Docker development. This script will install Docker (if missing), enable required kernel modules and sysctls, and verify the bridge/veth networking.

```bash
./scripts/dev-doctor.sh
```

This script is designed for Debian/Ubuntu-like systems. If you are on a different OS, or encounter issues, please refer to the Docker documentation for your specific environment.

### 2) One-command dev spin-up

Use the `dev` script for easy spin-up:

```bash
./dev up      # Builds, brings up, and detaches
./dev logs    # Follows logs
./dev down    # Tears down
```

Set these in `.env` (copied from `.env.example`):

* `INSTANCE_BASE`: your instance base URL
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
* Alembic migrations run via the `migrate` service. Note that `alembic.ini` leaves `sqlalchemy.url` empty; the `DATABASE_URL` environment variable is used instead.
* Add Prometheus to scrape `/metrics` as desired.

```
