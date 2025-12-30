"""
SENTINEL Data Validation Schemas
Using Pandera for production-grade data validation
"""

import pandera as pa
from pandera import Column, DataFrameSchema, Check
import pandas as pd
from typing import Dict


# Transaction Data Schema
transaction_schema = DataFrameSchema(
    {
        "transaction_id": Column(str, nullable=False, unique=True),
        "date": Column(str, nullable=False),  # Will be converted to datetime
        "company": Column(
            str,
            nullable=False,
            checks=Check.isin([
                "BBCA", "BBRI", "BMRI", "TLKM", "ASII",
                "UNVR", "ICBP", "GGRM", "INDF", "KLBF",
                "HMSP", "SMGR", "JPFA", "PTPP", "WIKA",
                "JSMR", "MNC", "PGAS", "ADRO", "ITMG"
            ])
        ),
        "insider_name": Column(str, nullable=False),
        "insider_role": Column(
            str,
            nullable=False,
            checks=Check.isin([
                "Director", "Commissioner", "Major Shareholder (>5%)", "CFO", "CEO"
            ])
        ),
        "action": Column(
            str,
            nullable=False,
            checks=Check.isin(["BUY", "SELL"])
        ),
        "volume": Column(
            int,
            nullable=False,
            checks=[
                Check.greater_than(0),
                Check.less_than(10_000_000)  # Reasonable upper bound
            ]
        ),
        "price": Column(
            int,
            nullable=False,
            checks=[
                Check.greater_than(0),
                Check.less_than(100_000)  # IDR 100k max
            ]
        ),
        "total_value": Column(int, nullable=False, checks=Check.greater_than(0)),
        "days_to_earnings": Column(
            int,
            nullable=False,
            checks=[
                Check.greater_than_or_equal_to(0),
                Check.less_than_or_equal_to(90)
            ]
        ),
        "is_suspicious": Column(bool, nullable=False),
        "violation_type": Column(str, nullable=True),  # None for normal transactions
    },
    strict=False,  # Allow additional columns (like derived features)
    coerce=True    # Try to coerce types
)


# News Article Schema
news_schema = DataFrameSchema(
    {
        "url": Column(str, nullable=False, unique=True),
        "title": Column(str, nullable=False, checks=Check.str_length(min_value=10)),
        "content": Column(str, nullable=False, checks=Check.str_length(min_value=50)),
        "date": Column(str, nullable=False),
        "source": Column(str, nullable=False),
        "keyword": Column(str, nullable=False),
        "scraped_at": Column(str, nullable=False),
    },
    strict=False,
    coerce=True
)


def validate_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate transaction data against schema

    Args:
        df: Input DataFrame

    Returns:
        Validated DataFrame

    Raises:
        pa.errors.SchemaError: If validation fails
    """
    try:
        validated_df = transaction_schema.validate(df, lazy=True)
        print("✅ Transaction data validation passed")
        return validated_df
    except pa.errors.SchemaErrors as err:
        print("❌ Validation failed:")
        print(err.failure_cases)
        raise


def validate_news_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate news article data against schema

    Args:
        df: Input DataFrame

    Returns:
        Validated DataFrame

    Raises:
        pa.errors.SchemaError: If validation fails
    """
    try:
        validated_df = news_schema.validate(df, lazy=True)
        print("✅ News data validation passed")
        return validated_df
    except pa.errors.SchemaErrors as err:
        print("❌ Validation failed:")
        print(err.failure_cases)
        raise


def get_data_quality_report(df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive data quality report

    Args:
        df: Input DataFrame

    Returns:
        Dict with quality metrics
    """
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

    # Numeric column statistics
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        report["numeric_stats"] = df[numeric_cols].describe().to_dict()

    # Categorical column distributions
    categorical_cols = df.select_dtypes(include=['object', 'bool']).columns
    if len(categorical_cols) > 0:
        report["categorical_distributions"] = {
            col: df[col].value_counts().head(10).to_dict()
            for col in categorical_cols
        }

    return report
