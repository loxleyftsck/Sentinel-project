"""
SENTINEL Project - Directory Structure Creator
Python script to create professional AI research project structure
"""

import os
from pathlib import Path

def create_directories(base_path):
    """Create all directories for the project structure."""
    
    directories = [
        # GitHub
        ".github/workflows",
        ".github/ISSUE_TEMPLATE",
        
        # Data layer
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
        
        # Notebooks
        "notebooks/1.0-exploratory",
        "notebooks/2.0-feature-engineering",
        "notebooks/3.0-modeling",
        "notebooks/4.0-evaluation",
        "notebooks/5.0-production",
        
        # Source code
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
    ]
    
    created = 0
    skipped = 0
    
    for dir_path in directories:
        full_path = Path(base_path) / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {dir_path}")
            created += 1
        else:
            print(f"⏭️  Skipped: {dir_path} (already exists)")
            skipped += 1
    
    return created, skipped

def create_python_packages(base_path):
    """Create __init__.py files for Python packages."""
    
    packages = [
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
    ]
    
    for pkg in packages:
        init_file = Path(base_path) / pkg / "__init__.py"
        if not init_file.exists():
            if pkg == "src/sentinel":
                content = '''"""
SENTINEL - Secure On-Premise Intelligent Surveillance System

A professional AI-powered compliance monitoring system for capital market surveillance.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
'''
            else:
                content = ""
            
            init_file.write_text(content, encoding="utf-8")
            print(f"✅ Created: {pkg}/__init__.py")

def create_gitkeep_files(base_path):
    """Create .gitkeep files for directories that should be tracked but empty."""
    
    gitkeep_dirs = [
        "data/raw/regulations",
        "data/interim/cleaned",
        "data/processed/features",
        "models/baselines",
        "models/registry",
        "experiments/mlruns",
        "monitoring/logs"
    ]
    
    for dir_path in gitkeep_dirs:
        gitkeep_file = Path(base_path) / dir_path / ".gitkeep"
        if not gitkeep_file.exists():
            gitkeep_file.touch()
            print(f"✅ Created: {dir_path}/.gitkeep")

def main():
    print("🏗️ Creating SENTINEL Professional Project Structure...")
    print("Based on: Cookiecutter Data Science V2 + Google ML + MLOps Standards\n")
    
    base_path = Path.cwd()
    
    # Create directories
    created, skipped = create_directories(base_path)
    
    print(f"\n📦 Creating Python package files...")
    create_python_packages(base_path)
    
    print(f"\n📌 Creating .gitkeep files...")
    create_gitkeep_files(base_path)
    
    print("\n" + "="*50)
    print("✅ Project Structure Created Successfully!")
    print("="*50)
    print(f"\n📂 Total directories created: {created}")
    print(f"⏭️  Directories skipped: {skipped}")
    print("\n🎯 Next Steps:")
    print("   1. Review PROJECT_STRUCTURE_GUIDE.md")
    print("   2. Initialize Git: git init")
    print("   3. Initialize DVC: dvc init")
    print("   4. Start development!")

if __name__ == "__main__":
    main()
