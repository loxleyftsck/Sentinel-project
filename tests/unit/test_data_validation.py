"""
Unit tests for SENTINEL data validation
"""

import pytest
import pandas as pd
import pandera as pa
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from sentinel.data.validation import (
    transaction_schema,
    news_schema,
    validate_transaction_data,
    validate_news_data,
    get_data_quality_report
)


class TestTransactionSchema:
    """Test suite for transaction schema validation"""

    def test_valid_transaction_data(self, valid_transaction_df):
        """Test that valid data passes validation"""
        validated = transaction_schema.validate(valid_transaction_df)
        assert len(validated) == len(valid_transaction_df)

    def test_invalid_company_fails(self, valid_transaction_df):
        """Test that invalid company code fails validation"""
        invalid_df = valid_transaction_df.copy()
        invalid_df.loc[0, 'company'] = 'INVALID'

        with pytest.raises(pa.errors.SchemaError):
            transaction_schema.validate(invalid_df, lazy=True)

    def test_negative_volume_fails(self, valid_transaction_df):
        """Test that negative volume fails validation"""
        invalid_df = valid_transaction_df.copy()
        invalid_df.loc[0, 'volume'] = -100

        with pytest.raises(pa.errors.SchemaError):
            transaction_schema.validate(invalid_df, lazy=True)

    def test_invalid_action_fails(self, valid_transaction_df):
        """Test that invalid action fails validation"""
        invalid_df = valid_transaction_df.copy()
        invalid_df.loc[0, 'action'] = 'HOLD'  # Not in ['BUY', 'SELL']

        with pytest.raises(pa.errors.SchemaError):
            transaction_schema.validate(invalid_df, lazy=True)

    def test_missing_required_column_fails(self, valid_transaction_df):
        """Test that missing required column fails"""
        invalid_df = valid_transaction_df.drop('transaction_id', axis=1)

        with pytest.raises(pa.errors.SchemaError):
            transaction_schema.validate(invalid_df)


class TestValidationFunctions:
    """Test validation utility functions"""

    def test_validate_transaction_data_success(self, valid_transaction_df):
        """Test validate_transaction_data with valid data"""
        result = validate_transaction_data(valid_transaction_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(valid_transaction_df)

    def test_validate_transaction_data_failure(self):
        """Test validate_transaction_data with invalid data"""
        invalid_df = pd.DataFrame({
            'transaction_id': ['T001'],
            'company': ['INVALID_COMPANY']
        })

        with pytest.raises(pa.errors.SchemaErrors):
            validate_transaction_data(invalid_df)

    def test_get_data_quality_report(self, valid_transaction_df):
        """Test data quality report generation"""
        report = get_data_quality_report(valid_transaction_df)

        # Check report structure
        assert 'total_rows' in report
        assert 'total_columns' in report
        assert 'missing_values' in report
        assert 'duplicate_rows' in report

        # Check values
        assert report['total_rows'] == len(valid_transaction_df)
        assert report['total_columns'] == len(valid_transaction_df.columns)
        assert isinstance(report['missing_values'], dict)


class TestNewsSchema:
    """Test suite for news schema validation"""

    def test_valid_news_data(self, valid_news_df):
        """Test that valid news data passes validation"""
        validated = news_schema.validate(valid_news_df)
        assert len(validated) == len(valid_news_df)

    def test_short_title_fails(self, valid_news_df):
        """Test that too-short title fails validation"""
        invalid_df = valid_news_df.copy()
        invalid_df.loc[0, 'title'] = 'Short'  # Less than 10 chars

        with pytest.raises(pa.errors.SchemaError):
            news_schema.validate(invalid_df, lazy=True)

    def test_short_content_fails(self, valid_news_df):
        """Test that too-short content fails validation"""
        invalid_df = valid_news_df.copy()
        invalid_df.loc[0, 'content'] = 'Too short content'  # Less than 50 chars

        with pytest.raises(pa.errors.SchemaError):
            news_schema.validate(invalid_df, lazy=True)


# Fixtures
@pytest.fixture
def valid_transaction_df():
    """Create valid transaction DataFrame"""
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
def valid_news_df():
    """Create valid news DataFrame"""
    return pd.DataFrame({
        'url': ['https://example.com/news1', 'https://example.com/news2'],
        'title': ['This is a valid news title that is long enough',
                  'Another valid news title for testing purposes'],
        'content': ['This is valid news content that is definitely longer than fifty characters required for validation.',
                    'Another piece of valid content that meets the minimum length requirement for testing.'],
        'date': ['2024-01-01', '2024-01-02'],
        'source': ['Kontan', 'Bisnis'],
        'keyword': ['insider trading', 'transaksi afiliasi'],
        'scraped_at': ['2024-01-01T10:00:00', '2024-01-01T11:00:00']
    })
