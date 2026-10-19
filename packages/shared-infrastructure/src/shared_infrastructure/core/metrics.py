import time
from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    Counter,
    Histogram,
    generate_latest,
)

# Shared metric collectors
REQUEST_COUNT = Counter(
    "workpilot_requests_total",
    "Total HTTP requests handled by the service",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION_SECONDS = Histogram(
    "workpilot_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)


def setup_prometheus_metrics(app: FastAPI, service_name: str | None = None) -> None:
    """
    Registers an asynchronous middleware to track HTTP latency and request counts,
    and mounts a dedicated /metrics endpoint for Prometheus scraping.
    """

    @app.middleware("http")
    async def prometheus_metrics_middleware(request: Request, call_next):
        # Do not record metrics for the Prometheus scrape itself or basic health checks to keep stats clean
        if request.url.path in ("/metrics", "/favicon.ico"):
            return await call_next(request)

        start_time = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration = time.perf_counter() - start_time
            endpoint = request.url.path

            # Best-effort route path matching to prevent high cardinality with path parameters (e.g. /users/{id})
            for route in request.app.routes:
                match, _ = route.matches(request.scope)
                if match:
                    endpoint = getattr(route, "path", endpoint)
                    break

            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status=status_code,
            ).inc()

            REQUEST_DURATION_SECONDS.labels(
                method=request.method,
                endpoint=endpoint,
            ).observe(duration)

    @app.get("/metrics", include_in_schema=False)
    def metrics_endpoint():
        """Prometheus metrics scrape target."""
        return Response(
            content=generate_latest(REGISTRY),
            media_type=CONTENT_TYPE_LATEST,
        )
