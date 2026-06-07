import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.logger import setup_logging
from app.routes import students_router, search_router

# ── Initialise logging before anything else ───────────────────────────────
setup_logging()
logger = logging.getLogger("main")

# ── Create FastAPI app ────────────────────────────────────────────────────
app = FastAPI(
    title="Student Manager API",
    description=(
        "A RESTful API for managing student records.\n\n"
        "**Features:**\n"
        "- Full CRUD operations\n"
        "- Pagination & sorting\n"
        "- Name search\n"
        "- Email validation\n"
        "- Data backup\n"
        "- Request logging\n"
    ),
    version="1.0.0",
    contact={
        "name": "Student Manager",
        "email": "admin@university.ac.ir",
    },
    license_info={"name": "MIT"},
)


# ── Request logging middleware ────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s → %d (%.1f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


# ── Global exception handler ──────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )


# ── Register routers ──────────────────────────────────────────────────────
app.include_router(students_router)
app.include_router(search_router)


# ── Home endpoint ─────────────────────────────────────────────────────────
@app.get("/", tags=["Home"], summary="Welcome message")
def home():
    """Returns a welcome message and useful links."""
    return {
        "message": "Welcome to Student Manager",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
    }
