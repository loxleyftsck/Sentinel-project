"""
Authentication Middleware
"""
from fastapi import Header, HTTPException
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Load API keys from environment
VALID_API_KEYS = set(os.getenv("API_KEYS", "dev-key-12345").split(","))


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from request header

    Args:
        x_api_key: API key from X-API-Key header

    Returns:
        Validated API key

    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "Missing API key",
                "message": "Please provide API key in X-API-Key header",
                "code": "MISSING_API_KEY"
            }
        )

    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "Invalid API key",
                "message": "The provided API key is not valid",
                "code": "INVALID_API_KEY"
            }
        )

    return x_api_key
