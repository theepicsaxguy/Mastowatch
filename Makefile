.PHONY: help dev backend-only prod build clean format lint typecheck test shell-db migration new-migration

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development environment with hot reload
	docker compose -f docker-compose.yml -f docker-compose.override.yml up --build

backend-only: ## Start only backend services (for frontend development)
	docker compose -f docker-compose.yml -f docker-compose.override.yml up --build api worker beat redis db

prod: ## Start production environment
	docker compose up --build

build: ## Build all images
	docker compose build

clean: ## Clean up containers and volumes
	docker compose down -v --remove-orphans
	docker system prune -f

format: ## Format code with black
	black --line-length 120 backend/app/ tests/

lint: ## Lint code with ruff
	ruff check backend/app/ tests/

typecheck: ## Type check with mypy
	mypy backend/app/

test: ## Run tests
	pytest

shell-db: ## Open database shell
	docker compose exec db psql -U postgres mastowatch

migration: ## Run database migrations
	docker compose run --rm migrate

new-migration: ## Create new migration (usage: make new-migration name="description")
	docker compose run --rm migrate alembic revision --autogenerate -m "$(name)"
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
	flake8 backend/app tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 backend/app tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black backend/app tests

format-check:
	black --check backend/app tests

typecheck:
	mypy backend/app/main.py backend/app/config.py backend/app/oauth.py --ignore-missing-imports

# Combined quality checks
check: lint format-check typecheck test check-httpx-usage

# Check for direct httpx usage outside /app/clients
check-httpx-usage:
	./scripts/check-httpx-usage.sh

# OpenAPI client management (using Git submodule)
update-api-spec:
    ./scripts/mastodon_api.sh update-schema

regenerate-client:
    ./scripts/mastodon_api.sh regenerate

update-mastodon-client:
    ./scripts/mastodon_api.sh update

api-client-status:
    ./scripts/mastodon_api.sh status

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
	docker compose run --rm migrate alembic revision --autogenerate -m "$(name)"

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
	@echo "  help             - Show this help message"

docker-build:
	DOCKER_BUILDKIT=1 docker compose build

docker-up:
	DOCKER_BUILDKIT=1 docker compose up
