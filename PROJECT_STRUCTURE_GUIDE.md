# 🏗️ SENTINEL Project Structure - Implementation Guide

## 📖 Overview

This document explains the professional AI research and engineering project structure for SENTINEL, based on global industry standards:

- **Cookiecutter Data Science V2** (2024)
- **Google ML Best Practices**
- **MLOps Industry Standards**
- **Quantitative Research Practices**

---

## 🎯 Design Principles

### 1. **Separation of Concerns**

- **Research** (`notebooks/`, `experiments/`) ≠ **Production** (`src/`, `models/`)
- **Data** (`data/`) ≠ **Code** (`src/`) ≠ **Configuration** (`config/`)
- **Training** (`training/`) ≠ **Inference** (`inference/`)

### 2. **Reproducibility First**

- All data transformations versioned (DVC)
- All experiments tracked (MLflow)
- All configurations declarative (YAML)
- All environments containerized (Docker)

### 3. **Production-Ready from Day 1**

- Modular, testable code
- Comprehensive test coverage
- CI/CD pipelines
- Monitoring & observability

---

## 📂 Directory Breakdown

### 🗂️ Data Layer (`data/`)

```
data/
├── raw/              # NEVER MODIFY - Original, immutable data
├── interim/          # Intermediate transformations
├── processed/        # Final, analysis-ready data
└── external/         # Third-party data sources
```

**Best Practices:**

- ✅ Version control with DVC, NOT Git
- ✅ Use `.gitignore` to exclude from Git
- ✅ Document data lineage in `dvc.yaml`
- ✅ Validate schemas with Pandera

**Example DVC Pipeline:**

```yaml
# dvc.yaml
stages:
  clean_data:
    cmd: python src/sentinel/data/preprocessing.py
    deps:
      - data/raw/transactions/
      - src/sentinel/data/preprocessing.py
    outs:
      - data/interim/cleaned/transactions.parquet
```

---

### 🧬 Models Layer (`models/`)

```
models/
├── baselines/        # Baseline models for comparison
├── rag/             # RAG model versions
│   ├── v1.0/
│   ├── v1.1/
│   └── production/  # Symlink to production model
├── embeddings/      # Embedding models
└── registry/        # Model metadata & lineage
```

**Model Versioning Strategy:**

- **Semantic versioning**: `v{major}.{minor}.{patch}`
- **Major**: Architecture changes
- **Minor**: Hyperparameter changes
- **Patch**: Bug fixes, retraining on same data

**Model Card Template:**

```markdown
# Model Card: RAG Detector v1.3

## Metadata
- **Date**: 2025-01-15
- **Author**: [Your Name]
- **MLflow Run ID**: abc123def456

## Performance
- Precision: 87% (95% CI: 84-90%)
- Recall: 82% (95% CI: 78-85%)
- F1 Score: 84.4%
```

---

### 📓 Research Layer (`notebooks/`)

**Naming Convention:** `{sequence}-{category}-{description}.ipynb`

Examples:

- `1.1-exploratory-transaction-eda.ipynb`
- `3.2-modeling-rag-experiments.ipynb`
- `4.1-evaluation-backtesting.ipynb`

**Notebook Structure:**

```python
# 1. IMPORTS
import pandas as pd
import mlflow

# 2. CONFIGURATION
CONFIG = {
    "experiment_name": "rag-v1.3",
    "random_state": 42
}

# 3. LOAD DATA
data = pd.read_parquet("data/processed/train.parquet")

# 4. EXPERIMENT (with MLflow tracking)
with mlflow.start_run(run_name="rag-baseline"):
    # Your code here
    mlflow.log_metric("accuracy", 0.87)

# 5. RESULTS
# Display visualizations, metrics
```

**Best Practices:**

- ✅ One notebook = One experiment
- ✅ Clear headings with markdown
- ✅ Log all experiments to MLflow
- ✅ Save outputs to `reports/figures/`
- ❌ Don't hardcode paths (use `config/`)
- ❌ Don't leave notebooks with errors

---

### 💻 Source Code Layer (`src/`)

**Package Structure:**

```
src/sentinel/
├── data/             # Data engineering
├── models/           # Model definitions
├── training/         # Training logic
├── evaluation/       # Evaluation logic
├── inference/        # Prediction logic
├── monitoring/       # ML monitoring
├── api/              # FastAPI application
└── utils/            # Utilities
```

**Code Quality Standards:**

1. **Type Hints (Mandatory)**

   ```python
   def predict(transaction: pd.DataFrame) -> Dict[str, float]:
       """Predict violation probability."""
       pass
   ```

2. **Docstrings (Google Style)**

   ```python
   def calculate_ic(predictions: np.ndarray, actuals: np.ndarray) -> float:
       """Calculate Information Coefficient.
       
       Args:
           predictions: Model predictions
           actuals: Ground truth labels
           
       Returns:
           Information Coefficient (correlation)
           
       Raises:
           ValueError: If arrays have different lengths
       """
       if len(predictions) != len(actuals):
           raise ValueError("Array length mismatch")
       return np.corrcoef(predictions, actuals)[0, 1]
   ```

3. **Error Handling**

   ```python
   from sentinel.utils.exceptions import ModelNotFoundError
   
   def load_model(model_path: Path) -> Model:
       if not model_path.exists():
           raise ModelNotFoundError(f"Model not found: {model_path}")
       return joblib.load(model_path)
   ```

---

### 🧪 Testing Layer (`tests/`)

**Test Categories:**

1. **Unit Tests** (`tests/unit/`)

   ```python
   # tests/unit/test_feature_engineering.py
   def test_zscore_calculation():
       data = pd.Series([10, 20, 30, 40, 50])
       result = calculate_zscore(data, value=30)
       assert result == 0.0  # Mean value
   ```

2. **Integration Tests** (`tests/integration/`)

   ```python
   # tests/integration/test_pipeline.py
   def test_end_to_end_pipeline():
       # Upload → Process → Predict → Store
       result = run_full_pipeline("sample_data.csv")
       assert result["status"] == "success"
   ```

3. **ML Tests** (`tests/ml_tests/`)

   ```python
   # tests/ml_tests/test_model_invariants.py
   def test_prediction_consistency():
       """Same input → Same output"""
       model = load_model()
       txn = create_sample_transaction()
       pred1 = model.predict(txn)
       pred2 = model.predict(txn)
       assert pred1 == pred2
   ```

**Test Coverage Target:** 80%+

```bash
# Run tests with coverage
pytest tests/ --cov=src/sentinel --cov-report=html
```

---

### ⚙️ Configuration Layer (`config/`)

**Configuration Hierarchy:**

```
base.yaml              # Shared settings
  ↓
development.yaml       # Dev overrides
staging.yaml           # Staging overrides
production.yaml        # Production overrides
```

**Example Configuration:**

```yaml
# config/model_config.yaml
model:
  name: "rag-detector"
  version: "1.3.0"
  
  embedding:
    model_name: "sentence-transformers/all-MiniLM-L6-v2"
    dimension: 384
  
  rag:
    chunk_size: 512
    chunk_overlap: 50
    top_k: 5
    
  llm:
    model: "llama3.1:8b-instruct-q4_K_M"
    temperature: 0.1
    max_tokens: 500

training:
  batch_size: 32
  epochs: 10
  learning_rate: 0.001
  random_seed: 42
```

**Loading Configuration:**

```python
from sentinel.utils.config import load_config

config = load_config("config/model_config.yaml")
chunk_size = config["model"]["rag"]["chunk_size"]
```

---

### 🔬 Experiments Layer (`experiments/`)

**Experiment Tracking with MLflow:**

```python
import mlflow
from sentinel.utils.config import load_config

# Load experiment config
config = load_config("experiments/experiment_configs/exp_003_ensemble.yaml")

# Start experiment
mlflow.set_experiment("sentinel-insider-trading")

with mlflow.start_run(run_name="ensemble-v1"):
    # Log parameters
    mlflow.log_params(config["model"])
    
    # Train model
    model = train_ensemble(config)
    
    # Evaluate
    metrics = evaluate(model, test_data)
    mlflow.log_metrics(metrics)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("reports/figures/confusion_matrix.png")
```

**Experiment Documentation:**

```markdown
# Experiment 003: Ensemble Model

## Hypothesis
Combining RAG + XGBoost will improve precision by 5%

## Configuration
- RAG model: v1.3
- XGBoost params: max_depth=5, n_estimators=100

## Results
- Precision: 89% (+2% vs RAG-only)
- Recall: 81% (-1% vs RAG-only)
- F1: 84.9% (+0.5%)

## Conclusion
Ensemble improves precision but slight recall trade-off.
DECISION: Deploy for low false-positive use cases.
```

---

### 📊 Monitoring Layer (`monitoring/`)

**Prometheus Metrics:**

```python
# src/sentinel/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
prediction_requests = Counter(
    'sentinel_predictions_total',
    'Total prediction requests',
    ['model_version', 'status']
)

# Performance metrics
inference_latency = Histogram(
    'sentinel_inference_seconds',
    'Inference latency',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# Model metrics
false_positive_rate = Gauge(
    'sentinel_false_positive_rate',
    'Rolling 24h false positive rate'
)
```

**Grafana Dashboard JSON:**

```json
{
  "dashboard": {
    "title": "SENTINEL Model Performance",
    "panels": [
      {
        "title": "Prediction Volume",
        "targets": [
          {
            "expr": "rate(sentinel_predictions_total[5m])"
          }
        ]
      }
    ]
  }
}
```

---

### 🚀 Deployment Layer (`infrastructure/`)

**Docker Multi-Stage Build:**

```dockerfile
# Dockerfile.api
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements-quant.txt .
RUN pip install --no-cache-dir -r requirements-quant.txt

FROM python:3.11-slim AS runtime

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ /app/src/
COPY config/ /app/config/

WORKDIR /app
CMD ["uvicorn", "src.sentinel.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Kubernetes Deployment:**

```yaml
# infrastructure/kubernetes/deployments/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentinel-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentinel-api
  template:
    metadata:
      labels:
        app: sentinel-api
    spec:
      containers:
      - name: api
        image: sentinel/api:v1.3.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: MLFLOW_TRACKING_URI
          valueFrom:
            configMapKeyRef:
              name: sentinel-config
              key: mlflow_uri
```

---

### 📚 Documentation Layer (`docs/`)

**MkDocs Configuration:**

```yaml
# mkdocs.yml
site_name: SENTINEL Documentation
theme:
  name: material
  palette:
    primary: indigo

nav:
  - Home: index.md
  - Architecture:
    - System Design: architecture/system_design.md
    - Data Flow: architecture/data_flow.md
  - API:
    - Endpoints: api/endpoints.md
  - Research:
    - Methodology: research/methodology.md
    - Model Cards: research/model_cards/
```

**Model Card Template:**

```markdown
# Model Card: RAG Detector v1.3

## Model Details
- **Developed by**: [Your Name]
- **Model type**: RAG-enhanced LLM
- **Version**: 1.3.0
- **Date**: 2025-01-15

## Intended Use
### Primary
- Automated insider trading pattern detection
- Compliance screening for securities regulators

### Out of Scope
- Fully automated enforcement (human review required)
- Non-Indonesian markets

## Training Data
- **Source**: IDX disclosures + synthetic data
- **Size**: 500 transactions (60/20/20 split)
- **Period**: 2020-2024

## Performance
- Precision: 87% (95% CI: 84-90%)
- Recall: 82% (95% CI: 78-85%)
- Information Coefficient: 0.31

## Limitations
- Designed for Indonesian markets only
- Requires 6 months historical data
- Performance degrades with novel schemes
```

---

## 🛠️ Automation (`Makefile`)

```makefile
# Makefile
.PHONY: setup test train deploy

# Environment setup
setup:
 python -m venv venv
 .\venv\Scripts\activate && pip install -r requirements-quant.txt
 docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Run tests
test:
 pytest tests/ --cov=src/sentinel --cov-report=html

# Format code
format:
 black src/ tests/
 isort src/ tests/

# Lint code
lint:
 flake8 src/ tests/
 mypy src/

# Train model
train:
 python scripts/training/train_rag.py --config config/model_config.yaml

# Run backtesting
backtest:
 python scripts/evaluation/run_backtesting.py

# Start API server
serve:
 uvicorn src.sentinel.api.main:app --reload --port 8001

# Build Docker images
build:
 docker build -f infrastructure/docker/Dockerfile.api -t sentinel/api:latest .

# Deploy to production
deploy:
 kubectl apply -f infrastructure/kubernetes/
```

---

## ✅ Best Practices Checklist

### Code Quality

- [ ] All functions have type hints
- [ ] All functions have Google-style docstrings
- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] No linting errors (Flake8)
- [ ] Type checking passes (mypy)

### Testing

- [ ] Unit test coverage > 80%
- [ ] Integration tests for critical paths
- [ ] ML behavioral tests (invariants)
- [ ] Load tests for API endpoints

### Data Management

- [ ] All data versioned with DVC
- [ ] Data schemas validated with Pandera
- [ ] Data lineage documented
- [ ] No data committed to Git

### Experiment Tracking

- [ ] All experiments logged to MLflow
- [ ] Experiment configs in YAML
- [ ] Results documented in markdown
- [ ] Models registered with metadata

### Documentation

- [ ] README.md comprehensive
- [ ] ARCHITECTURE.md up to date
- [ ] API documented (OpenAPI)
- [ ] Model cards for all versions
- [ ] Deployment guides current

### Deployment

- [ ] Dockerfiles multi-stage optimized
- [ ] Kubernetes manifests tested
- [ ] CI/CD pipelines configured
- [ ] Monitoring dashboards set up
- [ ] Alert rules defined

---

## 🎓 Learning Resources

### Books

- **"ML Engineering"** by Andriy Burkov
- **"Building Machine Learning Powered Applications"** by Emmanuel Ameisen
- **"Designing Data-Intensive Applications"** by Martin Kleppmann

### Online Courses

- **Made With ML** - MLOps best practices
- **Full Stack Deep Learning** - Production ML systems
- **Fast.ai** - Practical deep learning

### Templates

- **Cookiecutter Data Science**: <https://github.com/drivendataorg/cookiecutter-data-science>
- **ML Project Template**: <https://github.com/khuyentran1401/data-science-template>

---

## 📞 Support

For questions about this structure:

1. Check `docs/` for detailed guides
2. Review example projects in `examples/`
3. Open an issue on GitHub

---

**Remember:** A good project structure is invisible - it just works! 🎯
