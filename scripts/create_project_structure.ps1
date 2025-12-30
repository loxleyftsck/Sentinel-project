# ============================================
# SENTINEL Project - Directory Structure Creator
# PowerShell Script
# ============================================

Write-Host "🏗️ Creating SENTINEL Professional Project Structure..." -ForegroundColor Cyan
Write-Host "Based on: Cookiecutter Data Science V2 + Google ML + MLOps Standards`n" -ForegroundColor Gray

$baseDir = Get-Location

# Define directory structure
$directories = @(
    # GitHub
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
    
    # Data layer (gitignored, but structure created)
    "data/raw/regulations",
    "data/raw/transactions",
    "data/raw/news",
    "data/raw/market_data",
    "data/interim/cleaned",
    "data/interim/validated",
    "data/interim/augmented",
    "data/processed/features",
    "data/processed/embeddings",
    "data/processed/train_test_split",
    "data/external/benchmark",
    "data/external/third_party",
    
    # Models layer
    "models/baselines/rule_based",
    "models/baselines/statistical",
    "models/rag/v1.0",
    "models/rag/v1.1",
    "models/rag/production",
    "models/embeddings/sentence-transformers",
    "models/checkpoints",
    "models/registry",
    
    # Notebooks (research)
    "notebooks/1.0-exploratory",
    "notebooks/2.0-feature-engineering",
    "notebooks/3.0-modeling",
    "notebooks/4.0-evaluation",
    "notebooks/5.0-production",
    
    # Source code (production)
    "src/sentinel/data",
    "src/sentinel/models",
    "src/sentinel/training",
    "src/sentinel/evaluation",
    "src/sentinel/inference",
    "src/sentinel/monitoring",
    "src/sentinel/api/routes",
    "src/sentinel/utils",
    "src/sentinel/db",
    "src/pipelines",
    
    # Tests
    "tests/unit",
    "tests/integration",
    "tests/ml_tests",
    "tests/load",
    "tests/fixtures",
    
    # Configuration
    "config",
    
    # Scripts
    "scripts/setup",
    "scripts/data",
    "scripts/training",
    "scripts/evaluation",
    "scripts/deployment",
    
    # Experiments
    "experiments/mlruns",
    "experiments/mlartifacts",
    "experiments/experiment_configs",
    "experiments/results/metrics",
    "experiments/results/visualizations",
    "experiments/results/reports",
    
    # Monitoring
    "monitoring/prometheus",
    "monitoring/grafana/dashboards",
    "monitoring/grafana/datasources",
    "monitoring/logs",
    "monitoring/alerts",
    
    # Frontend
    "frontend/app/analyze",
    "frontend/app/regulations",
    "frontend/app/api/proxy",
    "frontend/components/ui",
    "frontend/lib",
    "frontend/public",
    
    # Infrastructure
    "infrastructure/docker",
    "infrastructure/kubernetes/deployments",
    "infrastructure/kubernetes/services",
    "infrastructure/kubernetes/ingress",
    "infrastructure/terraform",
    "infrastructure/ansible/playbooks",
    
    # Documentation
    "docs/architecture",
    "docs/api",
    "docs/research/model_cards",
    "docs/deployment",
    "docs/contributing",
    
    # Reports
    "reports/figures/confusion_matrices",
    "reports/figures/roc_curves",
    "reports/figures/feature_importance",
    "reports/backtesting",
    "reports/presentations"
)

# Create directories
$created = 0
$skipped = 0

foreach ($dir in $directories) {
    $fullPath = Join-Path $baseDir $dir
    
    if (!(Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        $created++
        Write-Host "✅ Created: $dir" -ForegroundColor Green
    }
    else {
        $skipped++
        Write-Host "⏭️  Skipped: $dir (already exists)" -ForegroundColor Yellow
    }
}

Write-Host "`n📊 Summary:" -ForegroundColor Cyan
Write-Host "   Created: $created directories" -ForegroundColor Green
Write-Host "   Skipped: $skipped directories" -ForegroundColor Yellow

# Create __init__.py files for Python packages
Write-Host "`n📦 Creating Python package files..." -ForegroundColor Cyan

$pythonPackages = @(
    "src",
    "src/sentinel",
    "src/sentinel/data",
    "src/sentinel/models",
    "src/sentinel/training",
    "src/sentinel/evaluation",
    "src/sentinel/inference",
    "src/sentinel/monitoring",
    "src/sentinel/api",
    "src/sentinel/api/routes",
    "src/sentinel/utils",
    "src/sentinel/db",
    "src/pipelines",
    "tests",
    "tests/unit",
    "tests/integration",
    "tests/ml_tests",
    "tests/load",
    "tests/fixtures"
)

foreach ($pkg in $pythonPackages) {
    $initFile = Join-Path $baseDir "$pkg/__init__.py"
    if (!(Test-Path $initFile)) {
        New-Item -ItemType File -Path $initFile -Force | Out-Null
        
        # Add docstring to main package
        if ($pkg -eq "src/sentinel") {
            @"
"""
SENTINEL - Secure On-Premise Intelligent Surveillance System

A professional AI-powered compliance monitoring system for capital market surveillance.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
"@ | Out-File -FilePath $initFile -Encoding UTF8
        }
        
        Write-Host "✅ Created: $pkg/__init__.py" -ForegroundColor Green
    }
}

# Create README files for key directories
Write-Host "`n📝 Creating README files..." -ForegroundColor Cyan

$readmeContent = @{
    "data/README.md"      = @"
# Data Directory

This directory contains all datasets used in the project.

## Structure

- **raw/**: Original, immutable data (NEVER modify)
- **interim/**: Intermediate transformations
- **processed/**: Final, analysis-ready data
- **external/**: Third-party data sources

## Important Notes

⚠️ **DO NOT** commit data files to Git
✅ Use DVC for data versioning
✅ Document data lineage in \`dvc.yaml\`

## Data Sources

1. **Regulations** (\`raw/regulations/\`)
   - POJK documents from ojk.go.id
   - IDX regulations from idx.co.id

2. **Transactions** (\`raw/transactions/\`)
   - Historical insider trading reports
   - Synthetic test data

3. **News** (\`raw/news/\`)
   - Scraped articles from financial news sites
   - Sentiment-labeled dataset

## Usage

\`\`\`python
import pandas as pd

# Load processed data
df = pd.read_parquet("data/processed/train.parquet")
\`\`\`
"@

    "models/README.md"    = @"
# Models Directory

Trained models and artifacts.

## Versioning Strategy

- **v{major}.{minor}.{patch}**
  - Major: Architecture changes
  - Minor: Hyperparameter changes
  - Patch: Bug fixes, retraining

## Production Model

The \`production/\` folder contains a symlink to the current production model.

\`\`\`bash
# Update production model
ln -sf ../rag/v1.3 production/current
\`\`\`

## Model Registry

All model metadata is tracked in \`registry/model_metadata.json\`:

\`\`\`json
{
  "model_id": "rag-v1.3",
  "created_at": "2025-01-15",
  "mlflow_run_id": "abc123",
  "performance": {
    "precision": 0.87,
    "recall": 0.82
  }
}
\`\`\`
"@

    "notebooks/README.md" = @"
# Notebooks Directory

Jupyter notebooks for research and experimentation.

## Naming Convention

\`{sequence}-{category}-{description}.ipynb\`

Examples:
- \`1.1-exploratory-data-eda.ipynb\`
- \`3.2-modeling-rag-experiments.ipynb\`

## Categories

1. **1.0-exploratory/** - Data exploration
2. **2.0-feature-engineering/** - Feature creation
3. **3.0-modeling/** - Model development
4. **4.0-evaluation/** - Model evaluation
5. **5.0-production/** - Production validation

## Best Practices

✅ One notebook = One experiment
✅ Log all experiments to MLflow
✅ Clear markdown headers
❌ No hardcoded paths
❌ No notebooks with errors
"@

    "src/README.md"       = @"
# Source Code

Production-ready Python package.

## Structure

- **data/**: Data engineering
- **models/**: Model definitions
- **training/**: Training logic
- **evaluation/**: Evaluation logic
- **inference/**: Prediction logic
- **monitoring/**: ML monitoring
- **api/**: FastAPI application
- **utils/**: Utilities
- **db/**: Database layer

## Code Quality

All code must follow:
- ✅ Type hints (mandatory)
- ✅ Google-style docstrings
- ✅ Black formatting
- ✅ Flake8 linting
- ✅ 80% test coverage

## Usage

\`\`\`python
from sentinel.models import RAGDetector
from sentinel.data import load_data

# Load data
data = load_data("data/processed/test.parquet")

# Load model
detector = RAGDetector.load("models/rag/production/current")

# Predict
predictions = detector.predict(data)
\`\`\`
"@
}

foreach ($file in $readmeContent.Keys) {
    $filePath = Join-Path $baseDir $file
    if (!(Test-Path $filePath)) {
        $readmeContent[$file] | Out-File -FilePath $filePath -Encoding UTF8
        Write-Host "✅ Created: $file" -ForegroundColor Green
    }
}

# Create .gitignore
Write-Host "`n🚫 Creating .gitignore..." -ForegroundColor Cyan
$gitignorePath = Join-Path $baseDir ".gitignore"

if (!(Test-Path $gitignorePath)) {
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Data (use DVC instead)
data/raw/**
data/interim/**
data/processed/**
data/external/**
!data/**/.gitkeep

# Models (use MLflow/DVC)
models/**
!models/**/.gitkeep

# Experiments
experiments/mlruns/**
experiments/mlartifacts/**
!experiments/**/.gitkeep

# Logs
*.log
monitoring/logs/**

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary
*.tmp
*.bak
*~
"@ | Out-File -FilePath $gitignorePath -Encoding UTF8
    Write-Host "✅ Created: .gitignore" -ForegroundColor Green
}

# Create .gitkeep files for empty directories
Write-Host "`n📌 Creating .gitkeep files..." -ForegroundColor Cyan

$gitkeepDirs = @(
    "data/raw/regulations",
    "data/interim/cleaned",
    "data/processed/features",
    "models/baselines",
    "models/registry",
    "experiments/mlruns",
    "monitoring/logs"
)

foreach ($dir in $gitkeepDirs) {
    $gitkeepPath = Join-Path $baseDir "$dir/.gitkeep"
    if (!(Test-Path $gitkeepPath)) {
        New-Item -ItemType File -Path $gitkeepPath -Force | Out-Null
        Write-Host "✅ Created: $dir/.gitkeep" -ForegroundColor Green
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ Project Structure Created Successfully!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📂 Total directories created: $created" -ForegroundColor White
Write-Host "📝 Documentation files: 4 README.md" -ForegroundColor White
Write-Host "🐍 Python packages: $($pythonPackages.Count) __init__.py" -ForegroundColor White
Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Review PROJECT_STRUCTURE_GUIDE.md" -ForegroundColor White
Write-Host "   2. Initialize Git: git init" -ForegroundColor White
Write-Host "   3. Initialize DVC: dvc init" -ForegroundColor White
Write-Host "   4. Start development!" -ForegroundColor White
