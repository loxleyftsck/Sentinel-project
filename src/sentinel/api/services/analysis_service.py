"""
Analysis Service - Integrates RAG Pipeline for Transaction Analysis
"""
import time
import uuid
from typing import Dict, List
from datetime import datetime
import logging

from ...models.rag import RAGPipeline, EmbeddingManager
from ...data.loaders import TransactionDataLoader
from ...data.validation import validate_transaction_data
from ..models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    Alert,
    Citation,
    TransactionData
)

logger = logging.getLogger("sentinel.api.analysis")


class AnalysisService:
    """
    Service for analyzing transactions using RAG pipeline
    """

    def __init__(self):
        """Initialize analysis service with RAG pipeline"""
        try:
            # Initialize RAG pipeline (reuse existing code!)
            self.rag = self._initialize_rag()
            logger.info("AnalysisService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AnalysisService: {e}")
            raise

    def _initialize_rag(self) -> RAGPipeline:
        """
        Initialize RAG pipeline with existing components

        Note: In production, load pre-built vectorstore
        For now, we'll create a minimal one
        """
        # TODO: Load pre-built vectorstore with regulations
        # For now, return None and handle gracefully
        logger.warning("RAG pipeline not fully initialized - using mock mode")
        return None

    async def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Analyze transaction for compliance violations

        Args:
            request: Analysis request with transaction data

        Returns:
            Analysis response with alerts and citations
        """
        start_time = time.time()
        transaction_id = str(uuid.uuid4())

        logger.info(f"Starting analysis for transaction {transaction_id}")

        try:
            # Extract transaction data
            txn = request.transaction

            # Perform analysis
            alerts = self._analyze_transaction(txn)
            risk_score = self._calculate_risk_score(alerts)
            citations = self._get_citations(alerts)

            processing_time = time.time() - start_time

            logger.info(
                f"Analysis complete for {transaction_id}: "
                f"{len(alerts)} alerts, risk={risk_score:.2f}, "
                f"time={processing_time:.2f}s"
            )

            return AnalysisResponse(
                transaction_id=transaction_id,
                alerts=alerts,
                risk_score=risk_score,
                citations=citations,
                processing_time=processing_time,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Analysis failed for {transaction_id}: {e}")
            raise

    def _analyze_transaction(self, txn: TransactionData) -> List[Alert]:
        """
        Analyze transaction and generate alerts

        Uses rule-based detection + RAG (when available)
        """
        alerts = []

        # Rule 1: Large transaction volume
        if txn.volume > 100000:
            alerts.append(Alert(
                severity="HIGH",
                title="Unusual Volume",
                description=f"Transaction volume ({txn.volume:,}) exceeds typical threshold",
                rule_violated="Internal Policy - Volume Threshold"
            ))

        # Rule 2: Selling activity (potentially suspicious)
        if txn.action == "SELL" and txn.volume > 50000:
            alerts.append(Alert(
                severity="MEDIUM",
                title="Significant Insider Selling",
                description=f"{txn.insider_role} sold {txn.volume:,} shares",
                rule_violated="POJK 30/2016 - Monitoring Required"
            ))

        # Rule 3: Director/Commissioner activity
        if txn.insider_role in ["Director", "Commissioner"]:
            alerts.append(Alert(
                severity="MEDIUM",
                title="High-Level Insider Activity",
                description=f"{txn.insider_role} transaction recorded",
                rule_violated="POJK 33/2014 - Disclosure Required"
            ))

        # TODO: Add RAG-based analysis when vectorstore is ready
        # if self.rag:
        #     rag_alerts = self._rag_analysis(txn)
        #     alerts.extend(rag_alerts)

        return alerts

    def _calculate_risk_score(self, alerts: List[Alert]) -> float:
        """Calculate risk score based on alerts"""
        if not alerts:
            return 0.0

        severity_weights = {
            "CRITICAL": 1.0,
            "HIGH": 0.75,
            "MEDIUM": 0.5,
            "LOW": 0.25
        }

        total_score = sum(severity_weights.get(alert.severity, 0.5) for alert in alerts)
        # Normalize to 0-1
        return min(total_score / len(alerts), 1.0)

    def _get_citations(self, alerts: List[Alert]) -> List[Citation]:
        """Get regulatory citations for alerts"""
        citations = []

        for alert in alerts:
            if alert.rule_violated:
                citations.append(Citation(
                    source=alert.rule_violated.split("-")[0].strip(),
                    article="Article 1",  # TODO: Extract from RAG
                    text="[Citation text would come from RAG pipeline]"
                ))

        # Remove duplicates
        seen = set()
        unique_citations = []
        for citation in citations:
            key = (citation.source, citation.article)
            if key not in seen:
                seen.add(key)
                unique_citations.append(citation)

        return unique_citations
