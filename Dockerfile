### --- Frontend build stage ---
FROM node:20-alpine AS fe
WORKDIR /fe
COPY frontend/ /fe/
RUN npm ci && npm run build

### --- Backend stage ---
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY alembic.ini /app/alembic.ini
COPY db/migrations /app/db/migrations
COPY rules.yml /app/rules.yml
COPY --from=fe /fe/dist /app/static/dashboard

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]