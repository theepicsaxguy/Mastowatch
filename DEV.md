# Mastowatch Development Setup

## Quick Start

### Option 1: Full Docker Environment
```bash
./dev up        # Start all services
./dev frontend  # Start frontend dev server (separate terminal)
./dev logs      # View logs
./dev down      # Stop everything
```

### Option 2: Local Development (Hybrid)
If you have Docker networking issues, use local development:
```bash
./dev local     # Start only DB/Redis in Docker
# Then follow the printed instructions to run the app locally
./dev local-down # Stop services when done
```

### Option 3: Frontend Only
```bash
./dev frontend  # Just work on the frontend
```

## Prerequisites

- **Docker & Docker Compose**: Required for all options
- **Node.js 20+**: Required for frontend development
- **Python 3.11+**: Required for local backend development

## Environment Setup

1. Copy environment file: `cp .env.example .env`
2. Edit `.env` with your Mastodon instance details:
   - `INSTANCE_BASE`: Your Mastodon instance URL
   - `ADMIN_TOKEN`: Admin access token from your instance
   - `BOT_TOKEN`: Bot access token from your instance
   - `API_KEY`: Random string for API authentication
   - `WEBHOOK_SECRET`: Random string for webhook validation

## Development Commands

| Command | Description |
|---------|-------------|
| `./dev up` | Start full development environment |
| `./dev down` | Stop and clean up all services |
| `./dev logs` | Show container logs |
| `./dev build` | Rebuild containers |
| `./dev frontend` | Start frontend dev server |
| `./dev local` | Start DB/Redis only, run app locally |
| `./dev local-down` | Stop local development services |

## Accessing Services

- **API**: http://localhost:8080
- **Frontend**: http://localhost:5173 (when running `./dev frontend`)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Troubleshooting

### Docker Network Issues
If you see "operation not supported" errors:
```bash
./dev local  # Use hybrid local development instead
```

### Database Issues
```bash
./dev down   # Clean up
./dev up     # Restart fresh
```

### Frontend Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Project Structure

```
app/           # Backend Python code
frontend/      # React/TypeScript frontend
db/migrations/ # Database migrations
scripts/       # Development scripts
docker-compose.yml      # Production Docker setup
docker-compose.dev.yml  # Development Docker setup (host networking)
```

## Common Workflows

### Backend Development
1. `./dev local` - Start services
2. Follow printed instructions to run locally
3. Make changes to `app/` files
4. Server auto-reloads with `--reload` flag

### Frontend Development
1. `./dev up` - Start backend services
2. `./dev frontend` - Start frontend dev server
3. Make changes to `frontend/src/` files
4. Hot reload handles updates

### Full Stack Development
1. `./dev up` - Start all services
2. `./dev frontend` - Start frontend dev server
3. Work on both frontend and backend
4. Use `./dev logs` to monitor backend
