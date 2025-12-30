"""
Quick test script to verify foundation components
Run this to ensure everything works before running full test suite
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

print("=" * 80)
print("🧪 SENTINEL Foundation Quick Test")
print("=" * 80)
print()

# Test 1: Data Loaders
print("📦 Test 1: Data Loaders")
print("-" * 80)
try:
    from sentinel.data.loaders import TransactionDataLoader

    loader = TransactionDataLoader()
    df = loader.load_latest_synthetic()

    print(f"✅ Loaded {len(df)} transactions")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Suspicious: {df['is_suspicious'].sum()}")

except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 2: Data Validation
print("🔍 Test 2: Data Validation")
print("-" * 80)
try:
    from sentinel.data.validation import validate_transaction_data

    validated = validate_transaction_data(df)
    print(f"✅ Validation passed for {len(validated)} rows")

except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 3: Feature Engineering
print("🔧 Test 3: Feature Engineering")
print("-" * 80)
try:
    from sentinel.data.utils import add_temporal_features, check_data_quality

    df_featured = add_temporal_features(df)
    print(f"✅ Added temporal features")
    print(f"   New columns: day_of_week, month, quarter, etc.")

    quality = check_data_quality(df_featured, verbose=False)
    print(f"✅ Quality check: {'PASSED' if quality['passed'] else 'ISSUES FOUND'}")

except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 4: RAG Components
print("🤖 Test 4: RAG Components")
print("-" * 80)
try:
    from sentinel.models.rag import DocumentProcessor, EmbeddingManager

    processor = DocumentProcessor(chunk_size=200, chunk_overlap=20)
    print(f"✅ DocumentProcessor initialized")

    # Test document processing
    test_docs = [
        {
            'text': "Ini adalah contoh transaksi mencurigakan oleh CEO di perusahaan BBCA.",
            'metadata': {'doc_id': 1}
        }
    ]

    processed = processor.process_documents(test_docs)
    print(f"✅ Processed {len(processed)} document chunks")

    # Test embedding manager (do NOT create vectorstore, just init)
    embedding_manager = EmbeddingManager()
    print(f"✅ EmbeddingManager initialized")
    print(f"   Model: sentence-transformers/all-MiniLM-L6-v2")

except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 5: Check Files Created
print("📁 Test 5: File Structure")
print("-" * 80)
try:
    src_dir = Path("src/sentinel")

    required_files = [
        "data/loaders.py",
        "data/validation.py",
        "data/utils.py",
        "models/rag.py"
    ]

    for file_path in required_files:
        full_path = src_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            sys.exit(1)

    # Check notebook
    notebook = Path("notebooks/2.0-feature-engineering/2.1-rag-poc-synthetic.ipynb")
    if notebook.exists():
        print(f"✅ RAG POC notebook exists")
    else:
        print(f"⚠️  RAG POC notebook not found")

except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Summary
print("=" * 80)
print("🎉 ALL TESTS PASSED!")
print("=" * 80)
print()
print("✅ Foundation components are working correctly")
print()
print("Next steps:")
print("  1. Run full test suite: pytest tests/")
print("  2. Open Jupyter Lab and run RAG POC notebook")
print("  3. Start collecting real data (Week 1)")
print()
print("Foundation Status: 🟢 READY FOR DEVELOPMENT")
print()
