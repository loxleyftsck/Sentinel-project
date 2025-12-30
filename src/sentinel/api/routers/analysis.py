"""
Analysis API Router
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
import logging

from ..models.schemas import AnalysisRequest, AnalysisResponse
from ..services.analysis_service import AnalysisService
from ..middleware.auth import verify_api_key

logger = logging.getLogger("sentinel.api.routers.analysis")

router = APIRouter(prefix="/analyze", tags=["Analysis"])


# Dependency: Get analysis service instance
def get_analysis_service() -> AnalysisService:
    """Dependency to get analysis service"""
    return AnalysisService()


@router.post("/", response_model=AnalysisResponse)
async def analyze_transaction(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze a transaction for compliance violations

    **Authentication**: Requires valid API key in `X-API-Key` header

    **Rate Limit**: 10 requests per minute

    **Request Body**:
    - transaction: Transaction data to analyze
    - options: Optional analysis options

    **Returns**:
    - alerts: List of compliance alerts
    - risk_score: Overall risk score (0-1)
    - citations: Regulatory citations
    - processing_time: Analysis time in seconds

    **Example**:
    ```json
    {
        "transaction": {
            "date": "2024-12-29T10:00:00",
            "company": "BBCA",
            "insider_name": "John Doe",
            "insider_role": "Director",
            "action": "SELL",
            "volume": 100000,
            "price": 9500
        }
    }
    ```
    """
    try:
        logger.info(f"Received analysis request for {request.transaction.company}")
        result = await service.analyze(request)
        return result

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Analysis failed",
                "message": str(e),
                "code": "ANALYSIS_ERROR"
            }
        )


@router.get("/health")
async def analysis_health():
    """Check if analysis service is healthy"""
    try:
        service = AnalysisService()
        return {
            "status": "healthy",
            "service": "analysis",
            "rag_available": service.rag is not None
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }
