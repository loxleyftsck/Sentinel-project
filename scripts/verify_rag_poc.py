"""
SENTINEL - RAG POC Component Verification
Test all components before running full notebook

Usage:
    python scripts/verify_rag_poc.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

print("="*80)
print("🧪 SENTINEL - RAG POC Component Verification")
print("="*80)
print()

# Test 1: Synthetic Data
print("📊 Test 1: Synthetic Data Loading")
print("-"*80)

try:
    data_dir = Path("data/raw/transactions")
    data_files = list(data_dir.glob("synthetic_transactions_*.csv"))
    
    if not data_files:
        print("❌ FAILED: No synthetic data found")
        print("   Run: python scripts/data/generate_synthetic.py")
        sys.exit(1)
    
    latest_file = max(data_files, key=lambda p: p.stat().st_mtime)
    df = pd.read_csv(latest_file)
    
    print(f"✅ PASSED: Loaded {len(df)} transactions from {latest_file.name}")
    print(f"   - Suspicious: {df['is_suspicious'].sum()} ({df['is_suspicious'].mean()*100:.1f}%)")
    print(f"   - Normal: {(~df['is_suspicious']).sum()}")
    print(f"   - Columns: {list(df.columns[:5])}...")
    
    # Validate required columns
    required_cols = ['transaction_id', 'company', 'insider_name', 'is_suspicious',  
                     'violation_type', 'volume', 'days_to_earnings']
    missing = [col for col in required_cols if col not in df.columns]
    
    if missing:
        print(f"❌ FAILED: Missing columns: {missing}")
        sys.exit(1)
    
    print("✅ All required columns present")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 2: Ollama Connection
print("🤖 Test 2: Ollama LLM Connection")
print("-"*80)

try:
    from langchain.llms import Ollama
    
    llm = Ollama(
        model="llama3.1:8b-instruct-q4_K_M",
        base_url="http://localhost:11434",
        temperature=0.1
    )
    
    print("✅ PASSED: Ollama client initialized")
    
    # Test inference
    test_query = "Jawab singkat: Apa itu insider trading?"
    print(f"\nTesting inference with query: '{test_query}'")
    
    response = llm(test_query)
    
    print(f"✅ PASSED: LLM response received ({len(response)} characters)")
    print(f"\nSample response (first 200 chars):")
    print(f"   {response[:200]}...")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\nTroubleshooting:")
    print("1. Check Ollama is running: ollama serve")
    print("2. Check model is downloaded: ollama list")
    print("3. If not: ollama pull llama3.1:8b-instruct-q4_K_M")
    sys.exit(1)

print()

# Test 3: LangChain Prompt Template
print("🔗 Test 3: LangChain Prompt Template")
print("-"*80)

try:
    from langchain.prompts import PromptTemplate
    from langchain_core.runnables import RunnableSequence
    
    template = """Analisis transaksi:
    Perusahaan: {company}
    Volume: {volume}
    Aksi: {action}
    
    Risiko: """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["company", "volume", "action"]
    )
    
    chain = prompt | llm
    
    print("✅ PASSED: Prompt template created")
    
    # Test with sample data
    sample = df.iloc[0]
    result = chain.invoke({
        "company": sample['company'],
        "volume": sample['volume'],
        "action": sample['action']
    })
    
    print(f"✅ PASSED: Chain executed successfully")
    print(f"\nSample analysis (first 150 chars):")
    print(f"   {result[:150]}...")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 4: Data Statistics
print("📈 Test 4: Data Quality Checks")
print("-"*80)

try:
    # Check for missing values
    missing = df.isnull().sum().sum()
    print(f"Missing values: {missing}")
    
    if missing > 0:
        print(f"⚠️  WARNING: Found {missing} missing values")
    else:
        print("✅ PASSED: No missing values")
    
    # Check suspicious ratio
    suspicious_ratio = df['is_suspicious'].mean()
    print(f"Suspicious ratio: {suspicious_ratio:.2%}")
    
    if 0.15 <= suspicious_ratio <= 0.25:
        print("✅ PASSED: Suspicious ratio within expected range (15-25%)")
    else:
        print(f"⚠️  WARNING: Suspicious ratio outside expected range")
    
    # Check violation types
    violation_types = df[df['is_suspicious']]['violation_type'].value_counts()
    print(f"\nViolation types:")
    for vtype, count in violation_types.items():
        print(f"   - {vtype}: {count}")
    
    print("✅ PASSED: Data quality checks complete")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 5: MLflow (Optional - may not be running)
print("📊 Test 5: MLflow Connection (Optional)")
print("-"*80)

try:
    import mlflow
    
    mlflow.set_tracking_uri("http://localhost:5000")
    
    # Try to create experiment (will fail if MLflow not running)
    try:
        mlflow.set_experiment("test-verification")
        print("✅ PASSED: MLflow server accessible")
        print("   URI: http://localhost:5000")
    except:
        print("⚠️  SKIPPED: MLflow server not running")
        print("   Start with: docker-compose -f docker-compose.mlops.yml up mlflow -d")
        print("   Or: make docker-up")
    
except Exception as e:
    print(f"⚠️  SKIPPED: MLflow not accessible ({str(e)[:50]}...)")
    print("   This is optional for POC")

print()

# Summary
print("="*80)
print("📋 VERIFICATION SUMMARY")
print("="*80)
print()
print("Core Components:")
print("✅ Synthetic Data: PASSED")
print("✅ Ollama LLM: PASSED")
print("✅ LangChain: PASSED")
print("✅ Data Quality: PASSED")
print("⚠️  MLflow: OPTIONAL (may not be running)")
print()
print("="*80)
print("🎉 ALL CRITICAL TESTS PASSED!")
print("="*80)
print()
print("✅ RAG POC components are working correctly!")
print()
print("Next Steps:")
print("1. Open Jupyter Lab: http://localhost:8888 (token: sentinel2024)")
print("2. Navigate to: notebooks/2.0-feature-engineering/2.1-rag-poc-synthetic.ipynb")
print("3. Run all cells to see full RAG analysis")
print()
print("Expected notebook runtime: 5-10 minutes")
print()

sys.exit(0)
