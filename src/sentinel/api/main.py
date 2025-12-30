"""
SENTINEL FastAPI Main Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

from .models.schemas import HealthResponse
from .routers import analysis

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel.api")
audit_logger = logging.getLogger("sentinel.audit")

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="SENTINEL API",
    description="AI-powered compliance monitoring system for insider trading detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - restrictive configuration
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only needed methods
    allow_headers=["Content-Type", "X-API-Key"],  # Only needed headers
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()

    # Log request
    logger.info(f"{request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Log response time
    process_time = time.time() - start_time
    logger.info(f"Completed in {process_time:.3f}s")

    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "code": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint

    Returns service status and Ollama availability
    """
    try:
        # Check Ollama status
        import requests
        ollama_response = requests.get("http://localhost:11434/api/tags", timeout=2)
        ollama_status = "healthy" if ollama_response.status_code == 200 else "unavailable"
    except:
        ollama_status = "unavailable"

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ollama_status=ollama_status
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": "SENTINEL API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "status": "operational"
    }


# Include routers
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "sentinel.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
