"""
SENTINEL Project - Installation Verification Script
Run this to verify all components are installed correctly
"""

import sys
import importlib
from typing import Dict, List, Tuple

def check_package(package_name: str, import_name: str = None) -> Tuple[bool, str]:
    """Check if a package is installed and return version."""
    try:
        module_name = import_name or package_name
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'unknown')
        return True, version
    except ImportError:
        return False, "NOT INSTALLED"

def main():
    print("=" * 60)
    print("🛡️ SENTINEL Installation Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"🐍 Python Version: {py_version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        return 1
    print("✅ Python version compatible")
    print()
    
    # Define packages to check
    packages: Dict[str, List[Tuple[str, str]]] = {
        "MLOps & Experiment Tracking": [
            ("mlflow", "mlflow"),
            ("dvc", "dvc"),
            ("evidently", "evidently"),
        ],
        "LLM & RAG Stack": [
            ("langchain", "langchain"),
            ("chromadb", "chromadb"),
            ("sentence-transformers", "sentence_transformers"),
            ("ollama", "ollama"),
        ],
        "Scientific Computing": [
            ("numpy", "numpy"),
            ("scipy", "scipy"),
            ("pandas", "pandas"),
            ("statsmodels", "statsmodels"),
        ],
        "Machine Learning": [
            ("scikit-learn", "sklearn"),
            ("xgboost", "xgboost"),
            ("lightgbm", "lightgbm"),
        ],
        "Model Explainability": [
            ("shap", "shap"),
        ],
        "Data Validation": [
            ("pandera", "pandera"),
        ],
        "API Framework": [
            ("fastapi", "fastapi"),
            ("uvicorn", "uvicorn"),
        ],
        "Visualization": [
            ("matplotlib", "matplotlib"),
            ("seaborn", "seaborn"),
            ("plotly", "plotly"),
        ],
        "Testing": [
            ("pytest", "pytest"),
            ("black", "black"),
        ],
        "Monitoring": [
            ("prometheus-client", "prometheus_client"),
        ],
    }
    
    total_packages = sum(len(pkgs) for pkgs in packages.values())
    installed_count = 0
    failed_packages = []
    
    for category, pkg_list in packages.items():
        print(f"📦 {category}")
        print("-" * 60)
        
        for package_name, import_name in pkg_list:
            success, version = check_package(package_name, import_name)
            
            if success:
                print(f"  ✅ {package_name:30s} {version}")
                installed_count += 1
            else:
                print(f"  ❌ {package_name:30s} {version}")
                failed_packages.append(package_name)
        
        print()
    
    # Summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"Total packages checked: {total_packages}")
    print(f"Installed: {installed_count} ✅")
    print(f"Missing: {len(failed_packages)} ❌")
    print()
    
    if failed_packages:
        print("⚠️  Missing packages:")
        for pkg in failed_packages:
            print(f"   - {pkg}")
        print()
        print("To install missing packages:")
        print("  pip install -r requirements-quant.txt")
        return 1
    else:
        print("🎉 All packages installed successfully!")
        print()
        print("🚀 Next steps:")
        print("  1. Ensure Ollama is running: ollama serve")
        print("  2. Download Ollama model: ollama pull llama3.1:8b-instruct-q4_K_M")
        print("  3. Start MLOps stack: docker-compose -f docker-compose.mlops.yml up -d")
        print("  4. Generate synthetic data: python scripts/data/generate_synthetic.py")
        print("  5. Verify RAG POC: python scripts/verify_rag_poc.py")
        print("  6. Start development: jupyter lab --port=8888")
        return 0

if __name__ == "__main__":
    sys.exit(main())
