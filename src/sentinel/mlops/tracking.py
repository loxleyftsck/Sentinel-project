"""
MLflow experiment tracking integration for SENTINEL

Usage:
    from sentinel.mlops.tracking import log_experiment

    log_experiment(
        experiment_name="transaction_analysis",
        params={"model": "llama3.1", "temperature": 0.7},
        metrics={"accuracy": 0.85, "f1_score": 0.82}
    )
"""

import mlflow
import os
from typing import Dict, Any, Optional
from datetime import datetime

# MLflow configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def log_experiment(
    experiment_name: str,
    params: Dict[str, Any],
    metrics: Dict[str, float],
    tags: Optional[Dict[str, str]] = None,
    artifacts: Optional[Dict[str, str]] = None
) -> str:
    """
    Log an experiment run to MLflow

    Args:
        experiment_name: Name of the experiment
        params: Parameters used in the run
        metrics: Metrics to log
        tags: Optional tags for the run
        artifacts: Optional artifacts to log (path: description)

    Returns:
        Run ID
    """
    # Set or create experiment
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id

    # Start run
    with mlflow.start_run(experiment_id=experiment_id) as run:
        # Log parameters
        mlflow.log_params(params)

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log tags
        if tags:
            mlflow.set_tags(tags)

        # Default tags
        mlflow.set_tag("timestamp", datetime.now().isoformat())
        mlflow.set_tag("project", "SENTINEL")

        # Log artifacts
        if artifacts:
            for path, description in artifacts.items():
                if os.path.exists(path):
                    mlflow.log_artifact(path)

        return run.info.run_id


def log_model_metrics(
    model_name: str,
    version: str,
    metrics: Dict[str, float]
):
    """Log model performance metrics"""
    experiment_name = f"model_{model_name}"

    return log_experiment(
        experiment_name=experiment_name,
        params={"model_name": model_name, "version": version},
        metrics=metrics,
        tags={"model_type": "RAG-LLM"}
    )


def log_analysis_run(
    transaction_id: str,
    risk_score: float,
    num_alerts: int,
    processing_time: float
):
    """Log transaction analysis metrics"""
    return log_experiment(
        experiment_name="transaction_analysis",
        params={"transaction_id": transaction_id},
        metrics={
            "risk_score": risk_score,
            "num_alerts": float(num_alerts),
            "processing_time": processing_time
        },
        tags={"run_type": "analysis"}
    )


# Example usage
if __name__ == "__main__":
    # Test MLflow connection
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        experiments = mlflow.search_experiments()
        print(f"✅ Connected to MLflow at {MLFLOW_TRACKING_URI}")
        print(f"   Found {len(experiments)} experiments")

        # Log test experiment
        run_id = log_experiment(
            experiment_name="test_experiment",
            params={"test_param": "value"},
            metrics={"test_metric": 0.95},
            tags={"environment": "development"}
        )
        print(f"✅ Logged test experiment: {run_id}")

    except Exception as e:
        print(f"❌ MLflow connection failed: {e}")
        print(f"   Make sure MLflow server is running:")
        print(f"   docker-compose -f docker-compose.mlops.yml up mlflow -d")
