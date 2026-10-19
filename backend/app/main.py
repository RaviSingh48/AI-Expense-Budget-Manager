import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import logger
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import DomainException
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.middleware.error_handler import (
    domain_exception_handler,
    db_exception_handler,
    global_exception_handler,
)
from app.routes.api_v1 import api_v1_router


# ---------------------------------------------------------------------------
# Lifespan
# Runs after Uvicorn binds the port.
# This is safe for Render's port detection.
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle managed by Uvicorn."""

    # -----------------------------------------------------------------------
    # Startup
    # -----------------------------------------------------------------------

    raw_env_url = os.getenv("DATABASE_URL")

    if raw_env_url:
        from app.core.database import mask_db_url

        logger.info(
            f"DATABASE_URL detected in environment: "
            f"{mask_db_url(raw_env_url)}"
        )
    else:
        logger.warning(
            "DATABASE_URL environment variable is NOT set. "
            "Falling back to the default database setting. "
            "IMPORTANT: Set DATABASE_URL in the Render Dashboard "
            "to your Render PostgreSQL Internal Database URL."
        )

    # -----------------------------------------------------------------------
    # Database table creation
    # Deferred until application startup so the port is already bound.
    # -----------------------------------------------------------------------

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified / created.")
    except Exception as exc:
        logger.error(f"DB create_all failed (non-fatal): {exc}")

    # -----------------------------------------------------------------------
    # ChromaDB / fallback vector store
    # Deferred for the same reason.
    # -----------------------------------------------------------------------

    try:
        from app.services.chroma_service import chroma_service  # noqa: F401

        logger.info("ChromaDB / vector-store initialised.")
    except Exception as exc:
        logger.error(f"Vector-store init failed (non-fatal): {exc}")

    # -----------------------------------------------------------------------
    # Startup complete
    # -----------------------------------------------------------------------

    logger.info(
        "Application startup complete — "
        f"HOST=0.0.0.0 "
        f"PORT={os.environ.get('PORT', settings.PORT)}"
    )

    yield

    # -----------------------------------------------------------------------
    # Shutdown
    # -----------------------------------------------------------------------

    logger.info("Application shutdown.")


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Personal Finance & Expense Advisor",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# CORS Configuration
#
# CORSMiddleware is added LAST so it becomes the outermost middleware
# at runtime.
#
# This allows:
#   - Production Vercel deployment
#   - Vercel preview deployments
#   - Local development
# ---------------------------------------------------------------------------

CORS_ORIGINS = [
    # Production Vercel deployment
    "https://ai-budget-expense-advisor.vercel.app",

    # FRONTEND_URL configured through environment variables
    settings.FRONTEND_URL,

    # Local development
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


# Remove empty values and duplicates while preserving order.
CORS_ORIGINS_DEDUPED = list(
    dict.fromkeys(
        origin.strip()
        for origin in CORS_ORIGINS
        if origin and origin.strip()
    )
)


app.add_middleware(
    CORSMiddleware,

    # Explicitly allowed origins
    allow_origins=CORS_ORIGINS_DEDUPED,

    # Allow Vercel preview deployments such as:
    # https://project-git-main-xxxx.vercel.app
    allow_origin_regex=r"https://.*\.vercel\.app",

    # Authentication / credentials support
    allow_credentials=True,

    # HTTP methods
    allow_methods=["*"],

    # Request headers
    allow_headers=["*"],

    # Response headers exposed to frontend
    expose_headers=["*"],
)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

# Request logging middleware
app.add_middleware(RequestLoggingMiddleware)


# ---------------------------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------------------------

app.add_exception_handler(
    DomainException,
    domain_exception_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    db_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# ---------------------------------------------------------------------------
# API Routers
# ---------------------------------------------------------------------------

app.include_router(api_v1_router)


# ---------------------------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "docs": "/docs",
        "api_version": "/api/v1",
    }


# ---------------------------------------------------------------------------
# Optional: Serve bundled frontend static files
#
# This is useful for local development or if the frontend is served
# through FastAPI.
#
# Your production frontend will still be deployed separately on Vercel.
# ---------------------------------------------------------------------------

_frontend_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "frontend",
    )
)


if os.path.exists(_frontend_dir):

    app.mount(
        "/static",
        StaticFiles(directory=_frontend_dir),
        name="static",
    )

    @app.get("/app", include_in_schema=False)
    def serve_frontend_index():
        return FileResponse(
            os.path.join(
                _frontend_dir,
                "index.html",
            )
        )


# ---------------------------------------------------------------------------
# Application Initialisation Log
# ---------------------------------------------------------------------------

logger.info(
    "FastAPI application initialised. "
    f"CORS origins: {CORS_ORIGINS_DEDUPED} "
    "+ regex *.vercel.app"
)


# ---------------------------------------------------------------------------
# Local Development Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )