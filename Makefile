# ==========================================
# SENTINEL Project - Makefile
# Automation for development workflow
# ==========================================

.PHONY: help setup install test lint format clean train evaluate serve build deploy

# Default target
help:
	@echo "🛡️ SENTINEL Project - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Create virtual environment and install dependencies"
	@echo "  make install        - Install package in development mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format         - Format code with Black and isort"
	@echo "  make lint           - Run linters (Flake8, mypy)"
	@echo "  make test           - Run test suite with coverage"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo ""
	@echo "Data & ML:"
	@echo "  make data           - Process raw data"
	@echo "  make features       - Generate features"
	@echo "  make train          - Train models"
	@echo "  make evaluate       - Evaluate models"
	@echo "  make backtest       - Run backtesting"
	@echo ""
	@echo "Development:"
	@echo "  make serve          - Start API server"
	@echo "  make jupyter        - Start Jupyter Lab"
	@echo "  make mlflow         - Start MLflow UI"
	@echo ""
	@echo "Deployment:"
	@echo "  make build          - Build Docker images"
	@echo "  make docker-up      - Start all Docker services"
	@echo "  make docker-down    - Stop all Docker services"
	@echo "  make deploy         - Deploy to production"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Clean temporary files"
	@echo "  make clean-all      - Clean everything (data, models, cache)"
	@echo ""

# ==========================================
# Setup & Installation
# ==========================================

setup:
	@echo "🔧 Creating virtual environment..."
	python -m venv venv
	@echo "📦 Installing dependencies..."
	.\venv\Scripts\python.exe -m pip install --upgrade pip
	.\venv\Scripts\pip.exe install -r requirements-quant.txt
	.\venv\Scripts\pip.exe install -r requirements-dev.txt
	@echo "✅ Setup complete! Activate with: .\venv\Scripts\Activate.ps1"

install:
	@echo "📦 Installing package in development mode..."
	pip install -e .
	@echo "✅ Package installed!"

# ==========================================
# Code Quality
# ==========================================

format:
	@echo "🎨 Formatting code..."
	black src/ tests/
	isort src/ tests/
	@echo "✅ Code formatted!"

lint:
	@echo "🔍 Running linters..."
	flake8 src/ tests/ --max-line-length=100 --exclude=venv,__pycache__
	mypy src/ --ignore-missing-imports
	@echo "✅ Linting complete!"

test:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ -v --cov=src/sentinel --cov-report=html --cov-report=term
	@echo "✅ Tests complete! Open htmlcov/index.html for coverage report"

test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/unit/ -v
	@echo "✅ Unit tests complete!"

test-integration:
	@echo "🧪 Running integration tests..."
	pytest tests/integration/ -v
	@echo "✅ Integration tests complete!"

# ==========================================
# Data & ML Pipeline
# ==========================================

data:
	@echo "📊 Processing raw data..."
	python scripts/data/collect_regulations.py
	python scripts/data/scrape_news.py
	python src/sentinel/data/preprocessing.py
	@echo "✅ Data processing complete!"

features:
	@echo "🔬 Generating features..."
	python src/sentinel/data/feature_engineering.py
	@echo "✅ Features generated!"

train:
	@echo "🎓 Training models..."
	python scripts/training/train_baseline.py
	python scripts/training/train_rag.py
	@echo "✅ Training complete! Check MLflow for results"

evaluate:
	@echo "📈 Evaluating models..."
	python scripts/evaluation/run_backtesting.py
	python scripts/evaluation/compare_models.py
	python scripts/evaluation/generate_report.py
	@echo "✅ Evaluation complete!"

backtest:
	@echo "📊 Running backtesting suite..."
	python scripts/evaluation/run_backtesting.py --full
	@echo "✅ Backtesting complete! Check reports/backtesting/"

# ==========================================
# Development
# ==========================================

serve:
	@echo "🚀 Starting API server..."
	uvicorn src.sentinel.api.main:app --reload --host 0.0.0.0 --port 8001

jupyter:
	@echo "📓 Starting Jupyter Lab..."
	jupyter lab --notebook-dir=notebooks

mlflow:
	@echo "📊 Starting MLflow UI..."
	mlflow ui --backend-store-uri sqlite:///mlflow.db

prometheus:
	@echo "📊 Starting Prometheus..."
	prometheus --config.file=monitoring/prometheus/prometheus.yml

grafana:
	@echo "📊 Starting Grafana..."
	grafana-server --config monitoring/grafana/grafana.ini

# ==========================================
# Docker & Deployment
# ==========================================

docker-up:
	@echo "🐳 Starting Docker services..."
	docker-compose -f docker-compose.mlops.yml up -d
	@echo "✅ Services started! Access:"
	@echo "   - MLflow:    http://localhost:5000"
	@echo "   - Grafana:   http://localhost:3001"
	@echo "   - Prometheus: http://localhost:9090"
	@echo "   - Jupyter:   http://localhost:8888"

docker-down:
	@echo "🐳 Stopping Docker services..."
	docker-compose -f docker-compose.mlops.yml down
	@echo "✅ Services stopped!"

docker-logs:
	docker-compose -f docker-compose.mlops.yml logs -f

build:
	@echo "🏗️ Building Docker images..."
	docker build -f infrastructure/docker/Dockerfile.api -t sentinel/api:latest .
	docker build -f infrastructure/docker/Dockerfile.training -t sentinel/training:latest .
	docker build -f infrastructure/docker/Dockerfile.frontend -t sentinel/frontend:latest .
	@echo "✅ Docker images built!"

deploy-staging:
	@echo "🚀 Deploying to staging..."
	kubectl apply -f infrastructure/kubernetes/ --namespace=staging
	@echo "✅ Deployed to staging!"

deploy-production:
	@echo "🚀 Deploying to production..."
	kubectl apply -f infrastructure/kubernetes/ --namespace=production
	@echo "✅ Deployed to production!"

# ==========================================
# Maintenance
# ==========================================

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name "*.egg-info" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "✅ Cleaned!"

clean-all: clean
	@echo "🧹 Cleaning everything (data, models, experiments)..."
	rm -rf data/processed/*
	rm -rf models/*/
	rm -rf experiments/mlruns/*
	rm -rf experiments/mlartifacts/*
	@echo "✅ Everything cleaned!"

# ==========================================
# CI/CD Workflow
# ==========================================

ci-test:
	@echo "🔄 Running CI test pipeline..."
	make lint
	make test
	@echo "✅ CI tests passed!"

cd-deploy:
	@echo "🔄 Running CD deployment pipeline..."
	make build
	make deploy-staging
	@echo "✅ CD deployment complete!"

# ==========================================
# DVC Pipeline
# ==========================================

dvc-pull:
	@echo "📥 Pulling data from DVC remote..."
	dvc pull
	@echo "✅ Data pulled!"

dvc-push:
	@echo "📤 Pushing data to DVC remote..."
	dvc push
	@echo "✅ Data pushed!"

dvc-repro:
	@echo "♻️ Reproducing DVC pipeline..."
	dvc repro
	@echo "✅ Pipeline reproduced!"

# ==========================================
# Documentation
# ==========================================

docs:
	@echo "📚 Building documentation..."
	mkdocs build
	@echo "✅ Documentation built! Open site/index.html"

docs-serve:
	@echo "📚 Serving documentation..."
	mkdocs serve

# ==========================================
# Monitoring & Health Checks
# ==========================================

health-check:
	@echo "🏥 Running health checks..."
	@echo "Checking API..."
	curl http://localhost:8001/health || echo "❌ API not responding"
	@echo "Checking MLflow..."
	curl http://localhost:5000/health || echo "❌ MLflow not responding"
	@echo "✅ Health check complete!"

load-test:
	@echo "⚡ Running load tests..."
	locust -f tests/load/locustfile.py --headless --users 50 --spawn-rate 5 --run-time 60s
	@echo "✅ Load test complete!"
