"""
SENTINEL Data Utilities
Helper functions for data processing and analysis
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path


def add_temporal_features(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
    """
    Add temporal features from date column

    Features added:
    - day_of_week (0=Monday, 6=Sunday)
    - month
    - quarter
    - is_quarter_end
    - is_month_end
    - year
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    df['day_of_week'] = df[date_col].dt.dayofweek
    df['month'] = df[date_col].dt.month
    df['quarter'] = df[date_col].dt.quarter
    df['is_quarter_end'] = df[date_col].dt.is_quarter_end
    df['is_month_end'] = df[date_col].dt.is_month_end
    df['year'] = df[date_col].dt.year

    return df


def add_statistical_features(
    df: pd.DataFrame,
    numeric_cols: List[str],
    group_by: str = 'company'
) -> pd.DataFrame:
    """
    Add statistical features (z-scores, percentiles) grouped by a column

    Args:
        df: Input DataFrame
        numeric_cols: Columns to compute stats for
        group_by: Column to group by

    Returns:
        DataFrame with added features
    """
    df = df.copy()

    for col in numeric_cols:
        # Z-score (normalized by group)
        # FIX #2: Return NaN instead of 0 when std=0 to indicate no variation
        df[f'{col}_zscore'] = df.groupby(group_by)[col].transform(
            lambda x: (x - x.mean()) / x.std() if x.std() > 0 else float('nan')
        )

        # Percentile rank
        df[f'{col}_percentile'] = df.groupby(group_by)[col].transform(
            lambda x: x.rank(pct=True)
        )

    return df


def detect_outliers(
    df: pd.DataFrame,
    columns: List[str],
    method: str = 'iqr',
    threshold: float = 1.5
) -> pd.DataFrame:
    """
    Detect outliers using IQR or Z-score method

    Args:
        df: Input DataFrame
        columns: Columns to check for outliers
        method: 'iqr' or 'zscore'
        threshold: IQR multiplier or z-score threshold

    Returns:
        DataFrame with boolean outlier columns
    """
    df = df.copy()

    for col in columns:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            df[f'{col}_is_outlier'] = (df[col] < lower_bound) | (df[col] > upper_bound)

        elif method == 'zscore':
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            df[f'{col}_is_outlier'] = z_scores > threshold

    return df


def create_lag_features(
    df: pd.DataFrame,
    columns: List[str],
    lags: List[int],
    group_by: Optional[str] = None
) -> pd.DataFrame:
    """
    Create lagged features (for time series)

    Args:
        df: Input DataFrame (should be sorted by time)
        columns: Columns to create lags for
        lags: List of lag periods (e.g., [1, 7, 30])
        group_by: Optional column to group by (e.g., 'company')

    Returns:
        DataFrame with lag features
    """
    df = df.copy()

    for col in columns:
        for lag in lags:
            if group_by:
                df[f'{col}_lag{lag}'] = df.groupby(group_by)[col].shift(lag)
            else:
                df[f'{col}_lag{lag}'] = df[col].shift(lag)

    return df


def create_rolling_features(
    df: pd.DataFrame,
    columns: List[str],
    windows: List[int],
    group_by: Optional[str] = None
) -> pd.DataFrame:
    """
    Create rolling window statistics

    Args:
        df: Input DataFrame (should be sorted by time)
        columns: Columns to compute rolling stats for
        windows: List of window sizes (e.g., [7, 30, 90])
        group_by: Optional column to group by

    Returns:
        DataFrame with rolling features
    """
    df = df.copy()

    for col in columns:
        for window in windows:
            if group_by:
                grouped = df.groupby(group_by)[col]
                df[f'{col}_rolling_mean_{window}'] = grouped.transform(
                    lambda x: x.rolling(window, min_periods=1).mean()
                )
                df[f'{col}_rolling_std_{window}'] = grouped.transform(
                    lambda x: x.rolling(window, min_periods=1).std()
                )
            else:
                df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window, min_periods=1).mean()
                df[f'{col}_rolling_std_{window}'] = df[col].rolling(window, min_periods=1).std()

    return df


def save_data_profile(df: pd.DataFrame, output_path: str) -> None:
    """
    Save comprehensive data profile to JSON

    Args:
        df: DataFrame to profile
        output_path: Path to save JSON file
    """
    profile = {
        "generated_at": datetime.now().isoformat(),
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage_mb": float(df.memory_usage(deep=True).sum() / 1024**2),
    }

    # Numeric summaries
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        profile["numeric_summary"] = numeric_df.describe().to_dict()

    # Categorical summaries
    categorical_df = df.select_dtypes(include=['object', 'category', 'bool'])
    if not categorical_df.empty:
        profile["categorical_summary"] = {
            col: df[col].value_counts().head(10).to_dict()
            for col in categorical_df.columns
        }

    # Save to file
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(profile, f, indent=2, default=str)

    print(f"✅ Data profile saved to: {output_path}")


def check_data_quality(df: pd.DataFrame, verbose: bool = True) -> Dict:
    """
    Comprehensive data quality checks

    Returns:
        Dict with quality metrics and issues
    """
    issues = []
    warnings = []

    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        issues.append(f"Missing values: {missing[missing > 0].to_dict()}")

    # Check for duplicates
    n_duplicates = df.duplicated().sum()
    if n_duplicates > 0:
        warnings.append(f"Duplicate rows: {n_duplicates}")

    # Check for constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        warnings.append(f"Constant columns: {constant_cols}")

    # Check data types
    object_cols = df.select_dtypes(include='object').columns
    if len(object_cols) > 0:
        warnings.append(f"Object dtype columns (consider optimization): {list(object_cols)}")

    quality_report = {
        "passed": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values_pct": (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
    }

    if verbose:
        if quality_report["passed"]:
            print("✅ Data quality checks passed")
        else:
            print("❌ Data quality issues found:")
            for issue in issues:
                print(f"  - {issue}")

        if warnings:
            print("⚠️  Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

    return quality_report
