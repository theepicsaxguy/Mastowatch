# Mastowatch Development Setup

## Quick Start

```bash
./dev up        # Start database services
./dev api       # Start API server (new terminal)
./dev frontend  # Start frontend dev server (new terminal) 
./dev down      # Stop everything when done
```

## Prerequisites

- **Docker**: Required for PostgreSQL and Redis
- **Python 3.11+**: For backend development
- **Node.js 20+**: For frontend development

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

## Development Commands

| Command | Description |
|---------|-------------|
| `./dev up` | Start database services (PostgreSQL + Redis) |
| `./dev down` | Stop and clean up all services |
| `./dev api` | Start API server (run after `up`) |
| `./dev frontend` | Start frontend dev server |
| `./dev logs` | Show container logs |
| `./dev shell` | Shell with development environment |

## Accessing Services

- **API**: http://localhost:8080
- **Frontend**: http://localhost:5173
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Typical Development Workflow

1. **Start databases**: `./dev up`
2. **Start API** (new terminal): `./dev api`
3. **Start frontend** (new terminal): `./dev frontend`
4. **Make changes** to code - both servers auto-reload
5. **Stop everything**: `./dev down`

## Architecture

This setup uses:
- **Docker with host networking** for databases (avoids networking issues)
- **Local Python environment** for the API server (fast iteration)
- **Local Node.js** for the frontend dev server (hot reload)

## Troubleshooting

### Database Connection Issues
```bash
./dev down   # Clean up
./dev up     # Restart fresh
```

### Python Environment Issues
```bash
rm -rf venv  # Remove virtual environment
./dev api    # Will recreate and install dependencies
```

### Frontend Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database Migrations
```bash
./dev shell  # Enter development shell
alembic upgrade head  # Run migrations manually
```

## Project Structure

```
app/           # Backend Python code
frontend/      # React/TypeScript frontend
db/migrations/ # Database migrations
venv/          # Python virtual environment (auto-created)
.env           # Environment variables (copy from .env.example)
```
