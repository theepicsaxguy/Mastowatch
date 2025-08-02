# Mastowatch Development Setup

## Quick Start

```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml up
```

**Or use the convenient Makefile shortcuts:**

```bash
make dev           # Start development environment
make dev-build     # Start with fresh build
make backend-only  # Start only backend services
make frontend-only # Start only frontend service
make logs          # View logs
make clean         # Stop and clean up
make help          # See all available commands
```

**Note:** The `migrate` service will automatically run `alembic upgrade head` before the API starts—no manual migration step needed. The first startup may take a moment while migrations complete.

## Prerequisites

- **Docker**: Required for PostgreSQL and Redis
- **Python 3.13+**: For backend development
- **Node.js 22+**: For frontend development

## Environment Setup

1. Copy environment file: `cp .env.example .env`
2. Edit `.env` with your Mastodon instance details:
   - `INSTANCE_BASE`: Your Mastodon instance URL
   - `ADMIN_TOKEN`: Admin access token from your instance
   - `BOT_TOKEN`: Bot access token from your instance
   - `API_KEY`: Random string for API authentication
   - `WEBHOOK_SECRET`: Random string for webhook validation

### Getting Mastodon Access Tokens

This application requires **two access tokens** from your Mastodon instance:

#### Creating Admin Token
1. Go to your Mastodon instance → **Settings → Development**
2. Click **"New Application"**
3. Set **Application name**: `MastoWatch Admin`
4. **Important**: Set scopes to `admin:read` and `admin:write`
5. Click **"Submit"**
6. Copy **"Your access token"** and paste as `ADMIN_TOKEN` in `.env`

#### Creating Bot Token  
1. Create another new application in the same place
2. Set **Application name**: `MastoWatch Bot`
3. **Important**: Set scopes to `read` and `write:reports`
4. Click **"Submit"**
5. Copy **"Your access token"** and paste as `BOT_TOKEN` in `.env`

**Note**: This app uses direct access tokens, not OAuth2 client credentials. You only need the "Your access token" value from each application, not the client key/secret.



## Project Structure

```
app/           # Backend Python code
frontend/      # React/TypeScript frontend
db/migrations/ # Database migrations
venv/          # Python virtual environment (auto-created)
.env           # Environment variables (copy from .env.example)
```
