"""Main FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import leads, enrichment, webhooks, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered lead generation and customer acquisition engine",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware - Allow all origins if CORS_ALLOW_ALL is True (for demos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.CORS_ALLOW_ALL else settings.ALLOWED_ORIGINS,
    allow_credentials=not settings.CORS_ALLOW_ALL,  # Can't use credentials with allow_origins=*
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])
app.include_router(enrichment.router, prefix="/api/v1/enrichment", tags=["Enrichment"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.PROJECT_NAME,
        "version": "0.1.0",
        "status": "active",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
