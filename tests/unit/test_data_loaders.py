"""
Unit tests for SENTINEL data loaders
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from sentinel.data.loaders import TransactionDataLoader, NewsDataLoader, RegulationDataLoader


class TestTransactionDataLoader:
    """Test suite for TransactionDataLoader"""

    def test_init_with_valid_directory(self):
        """Test initialization with valid directory"""
        loader = TransactionDataLoader(data_dir="data/raw/transactions")
        assert loader.data_dir.exists()

    def test_init_with_invalid_directory(self):
        """Test initialization with invalid directory"""
        with pytest.raises(FileNotFoundError):
            TransactionDataLoader(data_dir="nonexistent/directory")

    def test_load_latest_synthetic(self):
        """Test loading latest synthetic data file"""
        loader = TransactionDataLoader()
        df = loader.load_latest_synthetic()

        # Check DataFrame properties
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'transaction_id' in df.columns
        assert 'is_suspicious' in df.columns

    def test_validate_schema(self):
        """Test schema validation"""
        loader = TransactionDataLoader()
        df = loader.load_latest_synthetic()

        # Should not raise error if schema is valid
        loader._validate_schema(df)

    def test_missing_columns_raises_error(self):
        """Test that missing columns raise ValueError"""
        loader = TransactionDataLoader()

        # Create DataFrame with missing columns
        invalid_df = pd.DataFrame({
            'transaction_id': ['T001'],
            'company': ['BBCA']
        })

        with pytest.raises(ValueError, match="Missing required columns"):
            loader._validate_schema(invalid_df)

    def test_train_val_test_split(self):
        """Test train/val/test split"""
        loader = TransactionDataLoader()
        df = loader.load_latest_synthetic()

        splits = loader.get_train_val_test_split(
            df,
            train_ratio=0.6,
            val_ratio=0.2,
            test_ratio=0.2
        )

        # Check splits exist
        assert 'train' in splits
        assert 'val' in splits
        assert 'test' in splits

        # Check sizes are approximately correct
        total = len(df)
        assert abs(len(splits['train']) / total - 0.6) < 0.05
        assert abs(len(splits['val']) / total - 0.2) < 0.05
        assert abs(len(splits['test']) / total - 0.2) < 0.05

        # Check no data loss
        total_split = len(splits['train']) + len(splits['val']) + len(splits['test'])
        assert total_split == total

    def test_get_feature_matrix(self):
        """Test feature matrix extraction"""
        loader = TransactionDataLoader()
        df = loader.load_latest_synthetic()

        X, y = loader.get_feature_matrix(df)

        # Check shapes
        assert len(X) == len(df)
        assert len(y) == len(df)

        # Check feature columns exist
        assert 'volume' in X.columns
        assert 'price' in X.columns

        # Check target is boolean
        assert y.dtype == bool


class TestNewsDataLoader:
    """Test suite for NewsDataLoader"""

    def test_init_creates_directory(self):
        """Test that init creates directory if not exists"""
        loader = NewsDataLoader(data_dir="data/raw/news")
        assert loader.data_dir.exists()

    def test_load_articles_empty_directory(self):
        """Test loading from empty directory"""
        loader = NewsDataLoader()
        df = loader.load_articles()

        # Should return empty DataFrame without error
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


class TestRegulationDataLoader:
    """Test suite for RegulationDataLoader"""

    def test_init_creates_directory(self):
        """Test that init creates directory if not exists"""
        loader = RegulationDataLoader(data_dir="data/raw/regulations")
        assert loader.data_dir.exists()

    def test_list_available_pdfs(self):
        """Test listing PDF files"""
        loader = RegulationDataLoader()
        pdfs = loader.list_available_pdfs()

        # Should return list (may be empty)
        assert isinstance(pdfs, list)


# Fixtures
@pytest.fixture
def sample_transaction_df():
    """Create sample transaction DataFrame for testing"""
    return pd.DataFrame({
        'transaction_id': ['T001', 'T002', 'T003'],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'company': ['BBCA', 'BBRI', 'BMRI'],
        'insider_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'insider_role': ['CEO', 'CFO', 'Director'],
        'action': ['BUY', 'SELL', 'BUY'],
        'volume': [1000, 2000, 1500],
        'price': [10000, 15000, 12000],
        'total_value': [10000000, 30000000, 18000000],
        'days_to_earnings': [45, 10, 60],
        'is_suspicious': [False, True, False],
        'violation_type': [None, 'QUIET_PERIOD_VIOLATION', None]
    })


@pytest.fixture
def loader():
    """Create TransactionDataLoader instance"""
    return TransactionDataLoader()
