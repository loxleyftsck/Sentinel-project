"""
SENTINEL - Quick Test Script
Test your installation and verify all components are working
"""

import sys
from pathlib import Path

def test_imports():
    """Test critical package imports."""
    print("🧪 Testing Package Imports...")
    print("-" * 50)
    
    packages = {
        "mlflow": "MLflow",
        "langchain": "LangChain",
        "chromadb": "ChromaDB",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "sklearn": "scikit-learn",
        "fastapi": "FastAPI",
    }
    
    failed = []
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name:20s} - OK")
        except ImportError as e:
            print(f"❌ {name:20s} - FAILED: {e}")
            failed.append(name)
    
    return len(failed) == 0

def test_mlflow():
    """Test MLflow connection."""
    print("\n🔬 Testing MLflow...")
    print("-" * 50)
    
    try:
        import mlflow
        
        # Set tracking URI
        mlflow.set_tracking_uri("http://localhost:5000")
        
        # Try to create experiment
        experiment_name = "test-quick-verification"
        
        try:
            experiment_id = mlflow.create_experiment(experiment_name)
            print(f"✅ MLflow experiment created: {experiment_name}")
        except:
            # Experiment might already exist
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment:
                print(f"✅ MLflow experiment exists: {experiment_name}")
            else:
                print(f"⚠️  MLflow server not running (start with: make mlflow)")
                return False
        
        return True
    except Exception as e:
        print(f"❌ MLflow test failed: {e}")
        return False

def test_ollama():
    """Test Ollama installation."""
    print("\n🤖 Testing Ollama...")
    print("-" * 50)
    
    import subprocess
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ Ollama is installed")
            if "llama3.1" in result.stdout:
                print("✅ Llama 3.1 model available")
                return True
            else:
                print("⚠️  Llama 3.1 model not found")
                print("   Download with: ollama pull llama3.1:8b-instruct-q4_K_M")
                return False
        else:
            print(f"❌ Ollama error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        print("   Install with: winget install Ollama.Ollama")
        return False

def test_directories():
    """Test project structure."""
    print("\n📂 Testing Project Structure...")
    print("-" * 50)
    
    required_dirs = [
        "data/raw",
        "data/processed",
        "models/registry",
        "notebooks/1.0-exploratory",
        "src/sentinel",
        "tests/unit",
        "experiments/mlruns",
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path:30s} - Exists")
        else:
            print(f"❌ {dir_path:30s} - Missing")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 50)
    print("🛡️ SENTINEL - Quick Verification Test")
    print("=" * 50)
    print()
    
    results = {
        "imports": test_imports(),
        "directories": test_directories(),
        "ollama": test_ollama(),
    }
    
    # MLflow test optional (server might not be running)
    print("\n💡 Optional: MLflow test")
    print("   (Start MLflow first with: docker-compose up mlflow)")
    
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if all(results.values()):
        print("\n🎉 All core tests passed!")
        print("✅ Your environment is ready for development!")
        print("\nNext steps:")
        print("  1. Start Docker services: docker-compose up -d")
        print("  2. Start development: make jupyter")
        print("  3. Create your first notebook!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        print("\nQuick fixes:")
        if not results["ollama"]:
            print("  - Ollama: Run `ollama pull llama3.1:8b-instruct-q4_K_M`")
        if not results["imports"]:
            print("  - Packages: Run `pip install -r requirements-quant.txt`")
        if not results["directories"]:
            print("  - Structure: Run `python scripts/create_structure.py`")
    
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
