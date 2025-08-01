#!/bin/bash

# This script runs the Mastowatch application locally for development.

# Set environment variables for local development
export MST_BASE_URL="http://localhost:3000" # Replace with your Mastodon instance URL if needed
export BOT_TOKEN="YOUR_BOT_TOKEN" # Replace with your bot token
export ADMIN_TOKEN="YOUR_ADMIN_TOKEN" # Replace with your admin token
export DATABASE_URL="postgresql+psycopg://mastowatch:mastowatch@localhost:5432/mastowatch"
export REDIS_URL="redis://localhost:6379/0"
export DRY_RUN="true"
export BATCH_SIZE="80"

echo "Starting local Mastowatch development environment..."

# Start Docker Compose services for DB and Redis
echo "Starting database and Redis using Docker Compose..."
docker compose up -d db redis

# Wait for DB to be healthy
echo "Waiting for database to be healthy..."
docker compose run --rm migrate # This command waits for the DB healthcheck

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Apply Alembic migrations
echo "Applying Alembic migrations..."
alembic upgrade head

# Start the API server
echo "Starting API server..."
uvicorn app.main:app --host 0.0.0.0 --port 8080 &

# Start the Celery worker
echo "Starting Celery worker..."
celery -A app.tasks.celery_app worker --loglevel=INFO --concurrency=2 &

# Start the Celery beat scheduler
echo "Starting Celery beat scheduler..."
celery -A app.tasks.celery_app beat --loglevel=INFO &

echo "Mastowatch services started. Press Ctrl+C to stop."

# Trap CTRL+C to stop Docker Compose services on exit
trap "echo 'Stopping Docker Compose services...'; docker compose down; exit" INT TERM

wait
