# syntax=docker/dockerfile:1.4

FROM python:3.13-slim AS builder
WORKDIR /app
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential python3-dev \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.13-slim AS runtime
WORKDIR /app
RUN groupadd -r nonroot && useradd -r -g nonroot nonroot
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./alembic.ini
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
