"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class TransactionData(BaseModel):
    """Transaction data model"""
    date: datetime = Field(..., description="Transaction date")
    company: str = Field(..., description="Company ticker/name")
    insider_name: str = Field(..., description="Insider name")
    insider_role: Literal["Director", "Commissioner", "Major Shareholder"] = Field(
        ..., description="Insider role"
    )
    action: Literal["BUY", "SELL"] = Field(..., description="Transaction type")
    volume: int = Field(..., gt=0, description="Number of shares")
    price: float = Field(..., gt=0, description="Price per share")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-12-29T10:00:00",
                "company": "BBCA",
                "insider_name": "John Doe",
                "insider_role": "Director",
                "action": "SELL",
                "volume": 100000,
                "price": 9500
            }
        }


class Alert(BaseModel):
    """Alert model"""
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = Field(
        ..., description="Alert severity"
    )
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Alert description")
    rule_violated: Optional[str] = Field(None, description="Regulation violated")


class Citation(BaseModel):
    """Citation model"""
    source: str = Field(..., description="Source document")
    article: str = Field(..., description="Article/section number")
    text: str = Field(..., description="Relevant text snippet")


class AnalysisRequest(BaseModel):
    """Analysis request model"""
    transaction: TransactionData
    options: Optional[dict] = Field(
        default_factory=dict,
        description="Additional analysis options"
    )


class AnalysisResponse(BaseModel):
    """Analysis response model"""
    transaction_id: str = Field(..., description="Transaction ID")
    alerts: List[Alert] = Field(default_factory=list, description="Found alerts")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score (0-1)")
    citations: List[Citation] = Field(
        default_factory=list,
        description="Regulatory citations"
    )
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "tx_123456",
                "alerts": [
                    {
                        "severity": "HIGH",
                        "title": "Quiet Period Violation",
                        "description": "Transaction occurred 5 days before earnings announcement",
                        "rule_violated": "POJK 30/2016 Pasal 4"
                    }
                ],
                "risk_score": 0.78,
                "citations": [
                    {
                        "source": "POJK-30-2016.pdf",
                        "article": "Pasal 4 Ayat 1",
                        "text": "Direksi dilarang melakukan transaksi dalam periode 30 hari sebelum..."
                    }
                ],
                "processing_time": 2.34,
                "timestamp": "2024-12-29T10:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    ollama_status: str = Field(..., description="Ollama service status")
    timestamp: datetime = Field(default_factory=datetime.now)
