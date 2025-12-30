"""
SENTINEL Data Loading Utilities
Professional data loaders with validation and error handling
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TransactionDataLoader:
    """Load and validate transaction data with professional error handling"""

    def __init__(self, data_dir: str = "data/raw/transactions"):
        self.data_dir = Path(data_dir)

        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def load_latest_synthetic(self) -> pd.DataFrame:
        """Load the most recent synthetic transaction data"""
        pattern = "synthetic_transactions_*.csv"
        files = list(self.data_dir.glob(pattern))

        # FIX #1: Better error handling for missing files
        if not files:
            raise FileNotFoundError(
                f"No synthetic data files found in {self.data_dir}\n\n"
                f"📊 To generate data, run:\n"
                f"   python scripts/data/generate_synthetic.py\n\n"
                f"Or place CSV files matching '{pattern}' in: {self.data_dir}"
            )

        # Get most recent file
        try:
            latest_file = max(files, key=lambda p: p.stat().st_mtime)
        except (OSError, ValueError) as e:
            raise RuntimeError(f"Error accessing file metadata: {e}")

        logger.info(f"Loading: {latest_file.name}")
        df = pd.read_csv(latest_file)

        # Basic validation
        self._validate_schema(df)

        logger.info(f"Loaded {len(df)} transactions")
        logger.info(f"Suspicious: {df['is_suspicious'].sum()} ({df['is_suspicious'].mean()*100:.1f}%)")

        return df

    def load_specific_file(self, filename: str) -> pd.DataFrame:
        """Load a specific transaction file"""
        # FIX #8 (CRITICAL): Prevent path traversal attack
        # Validate filename doesn't contain path traversal patterns
        if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
            raise ValueError(
                f"Invalid filename: path traversal detected. "
                f"Filename must not contain '..' or start with '/' or '\\'"
            )

        filepath = self.data_dir / filename

        # Ensure resolved path is within data_dir (additional safety check)
        try:
            resolved_path = filepath.resolve()
            if not resolved_path.is_relative_to(self.data_dir.resolve()):
                raise ValueError(
                    f"Security violation: File must be within {self.data_dir}"
                )
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid file path: {e}")

        if not filepath.exists():
            raise FileNotFoundError(
                f"File not found: {filename}\n"
                f"Available files: {list(self.data_dir.glob('*.csv'))}"
            )

        logger.info(f"Loading: {filename}")
        df = pd.read_csv(filepath)
        self._validate_schema(df)

        return df

    def _validate_schema(self, df: pd.DataFrame) -> None:
        """Validate that DataFrame has required columns"""
        required_columns = [
            'transaction_id', 'company', 'insider_name', 'insider_role',
            'action', 'volume', 'price', 'total_value', 'days_to_earnings',
            'is_suspicious', 'violation_type'
        ]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        logger.info("✅ Schema validation passed")

    def get_train_val_test_split(
        self,
        df: pd.DataFrame,
        train_ratio: float = 0.6,
        val_ratio: float = 0.2,
        test_ratio: float = 0.2,
        sort_by: str = 'date'
    ) -> Dict[str, pd.DataFrame]:
        """
        Split data into train/val/test sets (temporal split)

        Args:
            df: Input DataFrame
            train_ratio: Proportion for training
            val_ratio: Proportion for validation
            test_ratio: Proportion for testing
            sort_by: Column to sort by (temporal split)

        Returns:
            Dict with 'train', 'val', 'test' DataFrames
        """
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.01, \
            "Ratios must sum to 1.0"

        # Sort by date for temporal split
        df_sorted = df.sort_values(sort_by).reset_index(drop=True)

        n = len(df_sorted)
        train_end = int(n * train_ratio)
        val_end = train_end + int(n * val_ratio)

        splits = {
            'train': df_sorted.iloc[:train_end].copy(),
            'val': df_sorted.iloc[train_end:val_end].copy(),
            'test': df_sorted.iloc[val_end:].copy()
        }

        logger.info(f"Split sizes - Train: {len(splits['train'])}, "
                   f"Val: {len(splits['val'])}, Test: {len(splits['test'])}")

        return splits

    def get_feature_matrix(
        self,
        df: pd.DataFrame,
        feature_cols: Optional[List[str]] = None
    ) -> tuple:
        """
        Extract feature matrix X and target y

        Args:
            df: Input DataFrame
            feature_cols: Columns to use as features (default: predefined list)

        Returns:
            (X, y) tuple
        """
        if feature_cols is None:
            feature_cols = [
                'volume', 'price', 'total_value', 'days_to_earnings',
                'volume_zscore', 'day_of_week', 'month',
                'is_quarter_end', 'action_buy'
            ]

        # Check columns exist
        missing = [col for col in feature_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing feature columns: {missing}")

        X = df[feature_cols].copy()
        y = df['is_suspicious'].copy()

        logger.info(f"Feature matrix shape: {X.shape}")
        logger.info(f"Target distribution: {y.value_counts().to_dict()}")

        return X, y


class NewsDataLoader:
    """Load and validate news article data"""

    def __init__(self, data_dir: str = "data/raw/news"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_articles(self, source: Optional[str] = None) -> pd.DataFrame:
        """
        Load news articles

        Args:
            source: Specific source to load (kontan, cnbc, bisnis) or None for all

        Returns:
            DataFrame with articles
        """
        if source:
            pattern = f"{source}_articles_*.csv"
        else:
            pattern = "*_articles_*.csv"

        files = list(self.data_dir.glob(pattern))

        if not files:
            logger.warning(f"No news data found in {self.data_dir}")
            logger.info("Run: python scripts/data/scrape_news.py")
            return pd.DataFrame()

        # Load all matching files
        dfs = []
        for f in files:
            df = pd.read_csv(f, encoding='utf-8-sig')
            dfs.append(df)

        combined = pd.concat(dfs, ignore_index=True)
        logger.info(f"Loaded {len(combined)} articles from {len(files)} files")

        return combined


class RegulationDataLoader:
    """Load and process regulatory documents (PDFs)"""

    def __init__(self, data_dir: str = "data/raw/regulations"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def list_available_pdfs(self) -> List[Path]:
        """List all PDF files in regulations directory"""
        pdfs = list(self.data_dir.glob("*.pdf"))
        logger.info(f"Found {len(pdfs)} PDF files")
        return pdfs

    def get_metadata(self) -> pd.DataFrame:
        """Load metadata about regulations from README or index file"""
        metadata_file = self.data_dir / "README.md"

        if not metadata_file.exists():
            logger.warning("No metadata file found")
            return pd.DataFrame()

        # TODO: Parse metadata from README
        return pd.DataFrame()


# Convenience functions
def load_synthetic_data() -> pd.DataFrame:
    """Quick function to load latest synthetic data"""
    loader = TransactionDataLoader()
    return loader.load_latest_synthetic()


def get_train_test_split(df: pd.DataFrame, test_size: float = 0.2) -> Dict[str, pd.DataFrame]:
    """Quick function for train/test split"""
    loader = TransactionDataLoader()
    return loader.get_train_val_test_split(
        df,
        train_ratio=1-test_size,
        val_ratio=0,
        test_ratio=test_size
    )
