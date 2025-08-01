from prometheus_client import Counter, Gauge, Histogram

accounts_scanned = Counter("sidecar_accounts_scanned_total", "Accounts scanned")
analyses_flagged = Counter("sidecar_analyses_flagged_total", "Analyses flagged", ["rule"])
reports_submitted = Counter("sidecar_reports_submitted_total", "Reports submitted", ["domain"])
http_errors = Counter("sidecar_http_errors_total", "HTTP errors", ["endpoint","code"])
queue_backlog = Gauge("sidecar_queue_backlog", "Queue backlog", ["queue"])
report_latency = Histogram("sidecar_report_latency_seconds", "Latency from analysis to report")
api_call_seconds = Histogram("sidecar_api_call_seconds", "API call duration seconds", ["endpoint"])
