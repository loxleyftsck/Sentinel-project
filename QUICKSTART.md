# SENTINEL Project - Quick Start Guide

## 🚀 Installation (Automated Setup)

### Option 1: Automated Setup (Recommended)

**Run the setup script:**

```powershell
# Navigate to project directory
cd "c:\Users\LENOVO\Documents\SENTINEL PROJECT"

# Run setup
.\scripts\setup_environment.ps1
```

The script will automatically:

- ✅ Check Python 3.11+ installation
- ✅ Create virtual environment
- ✅ Install all 80+ Python packages
- ✅ Install PyTorch with CUDA support (RTX 3060)
- ✅ Download Ollama and Llama 3.1 model
- ✅ Create project directory structure
- ✅ Configure environment variables (.env)
- ✅ Start Docker containers (MLflow, Grafana, Prometheus)

**Estimated time:** 15-20 minutes (depending on internet speed)

---

### Option 2: Manual Setup

#### Step 1: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Step 2: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install PyTorch (CUDA 11.8 for RTX 3060)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install all quantitative research libraries
pip install -r requirements-quant.txt
```

#### Step 3: Install Ollama

```powershell
# Download from: https://ollama.ai/download
# Or use winget:
winget install Ollama.Ollama

# Pull Llama 3.1 model
ollama pull llama3.1:8b-instruct-q4_K_M
```

#### Step 4: Start MLOps Infrastructure

```powershell
# Start all services
docker-compose -f docker-compose.mlops.yml up -d

# Verify services are running
docker-compose -f docker-compose.mlops.yml ps
```

---

## 🎯 Verify Installation

### Test Python Environment

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Test imports
python -c "import mlflow; print(f'MLflow: {mlflow.__version__}')"
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
python -c "import langchain; print(f'LangChain: {langchain.__version__}')"
python -c "import pandas, numpy, scipy, sklearn; print('✅ Scientific stack OK')"
```

### Test Ollama

```powershell
# Start Ollama server (if not already running)
ollama serve

# Test inference
ollama run llama3.1:8b-instruct-q4_K_M "Say hello in 5 words"
```

### Access Services

Open your browser:

- **MLflow UI**: <http://localhost:5000>
- **Grafana Dashboard**: <http://localhost:3001> (admin/admin123)
- **Prometheus Metrics**: <http://localhost:9090>
- **Jupyter Lab**: <http://localhost:8888> (token: sentinel123)
- **MinIO Console**: <http://localhost:9001> (minio/minio123)

---

## 📦 Installed Components

### Core ML & MLOps

- **MLflow 2.10.2** - Experiment tracking
- **DVC 3.48.0** - Data version control
- **Evidently 0.4.14** - ML monitoring & drift detection
- **Weights & Biases 0.16.3** - Experiment visualization

### LLM & RAG

- **LangChain 0.1.7** - LLM orchestration
- **Ollama 0.1.6** - Local LLM runtime
- **ChromaDB 0.4.22** - Vector database
- **Sentence Transformers 2.3.1** - Embeddings

### Quantitative Analysis

- **NumPy 1.26.3, SciPy 1.12.0, Pandas 2.2.0**
- **Statsmodels 0.14.1** - Statistical tests
- **Scikit-learn 1.4.0** - ML algorithms
- **XGBoost 2.0.3, LightGBM 4.3.0** - Gradient boosting

### Model Explainability

- **SHAP 0.44.1** - Feature attribution
- **LIME 0.2.0.1** - Local interpretability

### Data Validation

- **Pandera 0.18.0** - Schema validation
- **Great Expectations 0.18.8** - Data quality

### Testing & Quality

- **Pytest 7.4.4** - Unit testing
- **Locust 2.20.1** - Load testing
- **Black, Flake8, MyPy** - Code quality

---

## 🐳 Docker Services

| Service | Port | Credentials | Purpose |
|---------|------|-------------|---------|
| MLflow | 5000 | - | Experiment tracking |
| PostgreSQL | 5432 | sentinel/sentinel123 | Metadata storage |
| Redis | 6379 | redis123 | Caching & queues |
| Prometheus | 9090 | - | Metrics collection |
| Grafana | 3001 | admin/admin123 | Monitoring dashboards |
| ChromaDB | 8000 | sentinel-token-123 | Vector storage |
| Jupyter Lab | 8888 | sentinel123 | Research notebooks |
| MinIO | 9000, 9001 | minio/minio123 | Artifact storage |

---

## 🔧 Troubleshooting

### "Python not found"

```powershell
# Install Python 3.11+
winget install Python.Python.3.11
```

### "Docker not found"

```powershell
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop
```

### "CUDA not available"

```python
# Check NVIDIA driver
nvidia-smi

# Reinstall PyTorch with correct CUDA version
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### "Ollama connection refused"

```powershell
# Start Ollama server
ollama serve
```

### Docker containers fail to start

```powershell
# Check Docker is running
docker ps

# View container logs
docker-compose -f docker-compose.mlops.yml logs mlflow

# Restart services
docker-compose -f docker-compose.mlops.yml restart
```

---

## 📊 Next Steps

### 1. Test MLflow Tracking

```python
import mlflow

# Set tracking URI
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("test-experiment")

# Log a simple run
with mlflow.start_run():
    mlflow.log_param("test_param", 123)
    mlflow.log_metric("test_metric", 0.95)
    print("✅ MLflow tracking works!")
```

### 2. Test RAG Pipeline

```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Test vector store
vectorstore = Chroma(
    collection_name="test",
    embedding_function=embeddings,
    persist_directory="./chroma_test"
)

print("✅ RAG components work!")
```

### 3. Launch Jupyter Lab

```powershell
# Start Jupyter
jupyter lab

# Or use Docker Jupyter
# Already running at http://localhost:8888
```

### 4. Explore Research Notebooks

Navigate to `research/notebooks/` and start with:

- `01_eda.ipynb` - Exploratory data analysis
- `02_feature_engineering.ipynb` - Feature creation
- `03_model_selection.ipynb` - Model comparison

---

## 📚 Useful Commands

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Start all Docker services
docker-compose -f docker-compose.mlops.yml up -d

# Stop all services
docker-compose -f docker-compose.mlops.yml down

# View logs
docker-compose -f docker-compose.mlops.yml logs -f mlflow

# Clean up volumes (CAUTION: deletes all data)
docker-compose -f docker-compose.mlops.yml down -v

# Update dependencies
pip install -r requirements-quant.txt --upgrade
```

---

## ✅ Installation Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] All pip packages installed (80+ packages)
- [ ] PyTorch with CUDA support working
- [ ] Ollama installed and Llama 3.1 downloaded
- [ ] Docker Desktop installed and running
- [ ] All Docker containers running (8 services)
- [ ] MLflow UI accessible
- [ ] Grafana dashboard accessible
- [ ] Jupyter Lab accessible
- [ ] Test experiment logged to MLflow

**If all checked ✅ → You're ready to start quantitative research!** 🚀
