.PHONY: dev prod build clean logs test lint format migration

# Development shortcuts
dev:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up

dev-build:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up --build

dev-detached:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Backend only (for frontend development)
backend-only:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up db redis api worker beat migrate

# Frontend only (assumes backend is running separately)
frontend-only:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up frontend

# Production
prod:
	docker compose up

prod-build:
	docker compose up --build

# Utility commands
build:
	docker compose build

clean:
	docker compose down -v
	docker system prune -f

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

logs-worker:
	docker compose logs -f worker

logs-frontend:
	docker compose logs -f frontend

# Database operations
migration:
	docker compose run --rm migrate

# Testing and code quality
test:
	SKIP_STARTUP_VALIDATION=1 pytest

lint:
	flake8 app tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 app tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black app tests

format-check:
	black --check app tests

typecheck:
	mypy app/main.py app/config.py app/oauth.py --ignore-missing-imports

# Combined quality checks
check: lint format-check typecheck test check-httpx-usage

# Check for direct httpx usage outside /app/clients
check-httpx-usage:
	./scripts/check-httpx-usage.sh

# OpenAPI client management (using Git submodule)
update-api-spec:
	./scripts/update_mastodon_client.sh update-schema

regenerate-client:
	./scripts/update_mastodon_client.sh regenerate

update-mastodon-client:
	./scripts/update_mastodon_client.sh update

api-client-status:
	./scripts/update_mastodon_client.sh status

# Stop all services
stop:
	docker compose down

# Restart specific service
restart-api:
	docker compose restart api

restart-worker:
	docker compose restart worker

restart-frontend:
	docker compose restart frontend

# Show service status
status:
	docker compose ps

# Enter a running container
shell-api:
	docker compose exec api bash

shell-db:
	docker compose exec db psql -U mastowatch -d mastowatch

# Generate new migration
new-migration:
	docker compose run --rm api alembic revision --autogenerate -m "$(name)"

# Help
help:
	@echo "Available commands:"
	@echo "  dev              - Start development environment"
	@echo "  dev-build        - Start development environment with build"
	@echo "  dev-detached     - Start development environment in background"
	@echo "  backend-only     - Start only backend services (db, redis, api, worker, beat)"
	@echo "  frontend-only    - Start only frontend service"
	@echo "  prod             - Start production environment"
	@echo "  build            - Build all containers"
	@echo "  clean            - Stop containers and remove volumes"
	@echo "  logs             - Show logs for all services"
	@echo "  logs-<service>   - Show logs for specific service"
	@echo "  test             - Run Python tests"
	@echo "  lint             - Run code linting"
	@echo "  format           - Format code with black"
	@echo "  format-check     - Check code formatting"
	@echo "  typecheck        - Run type checking"
	@echo "  check            - Run all quality checks"
	@echo "  check-httpx-usage - Check for direct httpx usage outside /app/clients"
	@echo "  migration        - Run database migrations"
	@echo "  new-migration    - Generate new migration (use: make new-migration name='description')"
	@echo "  stop             - Stop all services"
	@echo "  status           - Show service status"
	@echo "  shell-<service>  - Enter running container shell"
	@echo "  update-api-spec      - Update OpenAPI spec from submodule"
	@echo "  regenerate-client    - Regenerate typed client from current spec"
	@echo "  update-mastodon-client - Full update: submodule + spec + client"
	@echo "  api-client-status    - Show current API client status"
	@echo "  help             - Show this help message"
