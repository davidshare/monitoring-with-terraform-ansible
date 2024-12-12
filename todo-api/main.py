from datetime import datetime
import time
import psutil
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from starlette.responses import Response
from app.core.config import settings
from app.core.database import engine
from app.core.database import Base
from app.endpoints.v1 import v1_router

# Custom metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', [
                        'method', 'status', 'path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds',
                            'HTTP Request Duration', ['method', 'status', 'path'])
REQUEST_IN_PROGRESS = Gauge(
    'http_requests_in_progress', 'HTTP Requests in progress', ['method', 'path'])

# System metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes',
                     'Current memory usage in bytes')

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)
origins = [
    settings.FRONTEND_ORIGIN,  # Allow your frontend's origin
    # Add other origins if needed
]

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    method = request.method
    path = request.url.path

    REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    status = response.status_code
    REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=status,
                           path=path).observe(duration)
    REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

    return response


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/api", status_code=200)
def api():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "welcome to todos api"
    }


@app.get("/health", status_code=200)
def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/metrics")
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)


# Include API router
app.include_router(v1_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
