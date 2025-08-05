# syntax=docker/dockerfile:1.4

# Stage 1: Builder
FROM python:3.10-slim as builder
WORKDIR /app
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential python3-dev \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

# Stage 2: Runtime
FROM gcr.io/distroless/python3
WORKDIR /app
COPY --from=builder /app /app
CMD ["app/main.py"]  # Adjust as needed
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
