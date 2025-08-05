# syntax=docker/dockerfile:1.4

FROM python:3.13-slim AS builder
WORKDIR /backend
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential python3-dev \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --wheel-dir=/wheels -r requirements.txt \
 && pip install --no-cache-dir /wheels/*.whl \
 && rm -rf /wheels

FROM node:22-alpine AS fe
WORKDIR /backend/frontend
COPY frontend/package*.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY frontend/ .
RUN npm run build

FROM gcr.io/distroless/python3-debian12 AS runtime
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY app /app/app
COPY migrations /app/db/migrations
COPY --from=fe /backend/frontend/dist /app/static/dashboard
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["uvicorn","app.main:app","--host=0.0.0.0","--port=8080"]
