"""
SENTINEL - Synthetic Transaction Data Generator
Generate realistic synthetic insider trading transaction data

Usage:
    python scripts/data/generate_synthetic.py --num-transactions 500
    python scripts/data/generate_synthetic.py --suspicious-ratio 0.2
"""

import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import pandas as pd
import numpy as np
from faker import Faker

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker('id_ID')  # Indonesian locale
np.random.seed(42)


class TransactionGenerator:
    """Generate synthetic insider trading transactions"""
    
    # Indonesian companies (top 30 by market cap)
    COMPANIES = [
        "BBCA", "BBRI", "BMRI", "TLKM", "ASII",
        "UNVR", "ICBP", "GGRM", "INDF", "KLBF",
        "HMSP", "SMGR", "JPFA", "PTPP", "WIKA",
        "JSMR", "MNC", "PGAS", "ADRO", "ITMG"
    ]
    
    INSIDER_ROLES = [
        "Director", 
        "Commissioner", 
        "Major Shareholder (>5%)",
        "CFO",
        "CEO"
    ]
    
    ACTIONS = ["BUY", "SELL"]
    
    def __init__(self, output_dir: str = "data/raw/transactions"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.transactions = []
    
    def generate_normal_transaction(self) -> Dict:
        """Generate a normal (non-suspicious) transaction"""
        company = np.random.choice(self.COMPANIES)
        
        # Normal transaction characteristics
        date = fake.date_between(start_date='-2y', end_date='today')
        
        # Not close to earnings (safe timing)
        # Assume earnings every quarter
        quarter_end = pd.Timestamp(date).quarter
        days_to_earnings = np.random.randint(45, 85)  # Well before/after earnings
        
        volume = int(np.random.lognormal(10, 1.5))  # ~1000-50000 shares
        price = int(np.random.uniform(1000, 50000))  # IDR 1k-50k
        
        return {
            'transaction_id': fake.uuid4(),
            'date': date.isoformat(),
            'company': company,
            'insider_name': fake.name(),
            'insider_role': np.random.choice(self.INSIDER_ROLES),
            'action': np.random.choice(self.ACTIONS),
            'volume': volume,
            'price': price,
            'total_value': volume * price,
            'days_to_earnings': days_to_earnings,
            'is_suspicious': False,
            'violation_type': None,
            'reason': 'Normal transaction pattern'
        }
    
    def generate_suspicious_transaction(self) -> Dict:
        """Generate a suspicious transaction"""
        company = np.random.choice(self.COMPANIES)
        
        # Choose violation type
        violation_types = [
            'QUIET_PERIOD',
            'UNUSUAL_VOLUME', 
            'TIMING_SUSPICIOUS',
            'MULTIPLE_VIOLATIONS'
        ]
        violation = np.random.choice(violation_types)
        
        base_txn = self.generate_normal_transaction()
        
        if violation == 'QUIET_PERIOD':
            # Transaction within 30 days before earnings
            days_to_earnings = np.random.randint(1, 30)
            base_txn['days_to_earnings'] = days_to_earnings
            base_txn['is_suspicious'] = True
            base_txn['violation_type'] = 'QUIET_PERIOD_VIOLATION'
            base_txn['reason'] = f'Transaction {days_to_earnings} days before earnings announcement'
        
        elif violation == 'UNUSUAL_VOLUME':
            # Abnormally high volume (3-5x normal)
            multiplier = np.random.uniform(3.0, 5.0)
            base_txn['volume'] = int(base_txn['volume'] * multiplier)
            base_txn['total_value'] = base_txn['volume'] * base_txn['price']
            base_txn['is_suspicious'] = True
            base_txn['violation_type'] = 'UNUSUAL_VOLUME'
            base_txn['reason'] = f'Volume {multiplier:.1f}x above historical average'
        
        elif violation == 'TIMING_SUSPICIOUS':
            # Transaction before major news/price movement
            days_before_news = np.random.randint(1, 7)
            base_txn['is_suspicious'] = True
            base_txn['violation_type'] = 'TIMING_PATTERN'
            base_txn['reason'] = f'Transaction {days_before_news} days before material information disclosure'
        
        else:  # MULTIPLE_VIOLATIONS
            # Combine violations
            days_to_earnings = np.random.randint(1, 30)
            multiplier = np.random.uniform(2.5, 4.0)
            
            base_txn['days_to_earnings'] = days_to_earnings
            base_txn['volume'] = int(base_txn['volume'] * multiplier)
            base_txn['total_value'] = base_txn['volume'] * base_txn['price']
            base_txn['is_suspicious'] = True
            base_txn['violation_type'] = 'MULTIPLE_VIOLATIONS'
            base_txn['reason'] = f'Quiet period + volume anomaly ({multiplier:.1f}x normal)'
        
        return base_txn
    
    def generate_dataset(
        self,
        num_transactions: int = 500,
        suspicious_ratio: float = 0.2
    ) -> pd.DataFrame:
        """Generate complete dataset"""
        num_suspicious = int(num_transactions * suspicious_ratio)
        num_normal = num_transactions - num_suspicious
        
        logger.info(f"Generating {num_transactions} transactions:")
        logger.info(f"  - Normal: {num_normal}")
        logger.info(f"  - Suspicious: {num_suspicious}")
        
        # Generate transactions
        transactions = []
        
        for i in range(num_normal):
            transactions.append(self.generate_normal_transaction())
            if (i + 1) % 100 == 0:
                logger.info(f"  Generated {i + 1} normal transactions")
        
        for i in range(num_suspicious):
            transactions.append(self.generate_suspicious_transaction())
            if (i + 1) % 20 == 0:
                logger.info(f"  Generated {i + 1} suspicious transactions")
        
        # Create DataFrame
        df = pd.DataFrame(transactions)
        
        # Add additional features
        df = self.add_derived_features(df)
        
        # Shuffle
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return df
    
    def add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features for modeling"""
        
        # Volume z-score (normalized by company)
        df['volume_zscore'] = df.groupby('company')['volume'].transform(
            lambda x: (x - x.mean()) / x.std()
        )
        
        # Day of week
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        
        # Month
        df['month'] = pd.to_datetime(df['date']).dt.month
        
        # Is quarter end
        df['is_quarter_end'] = pd.to_datetime(df['date']).dt.is_quarter_end
        
        # Action binary
        df['action_buy'] = (df['action'] == 'BUY').astype(int)
        
        return df
    
    def save_dataset(self, df: pd.DataFrame, suffix: str = "v1"):
        """Save dataset to CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"synthetic_transactions_{suffix}_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        logger.info(f"✅ Saved {len(df)} transactions to {filename}")
        
        # Generate data quality report
        self.generate_report(df, filename)
        
        return filename
    
    def generate_report(self, df: pd.DataFrame, data_file: Path):
        """Generate data quality report"""
        report_file = data_file.parent / f"DATA_REPORT_{data_file.stem}.md"
        
        report = f"""# Synthetic Transaction Data Report

**Generated**: {datetime.now().isoformat()}  
**File**: {data_file.name}

## Summary Statistics

- **Total Transactions**: {len(df)}
- **Suspicious Transactions**: {df['is_suspicious'].sum()} ({df['is_suspicious'].mean()*100:.1f}%)
- **Normal Transactions**: {(~df['is_suspicious']).sum()} ({(~df['is_suspicious']).mean()*100:.1f}%)

## Violation Types

{df[df['is_suspicious']]['violation_type'].value_counts().to_markdown()}

## Company Distribution

{df['company'].value_counts().head(10).to_markdown()}

## Insider Roles

{df['insider_role'].value_counts().to_markdown()}

## Action Distribution

{df['action'].value_counts().to_markdown()}

## Volume Statistics

- **Mean**: {df['volume'].mean():.0f}
- **Median**: {df['volume'].median():.0f}
- **Std Dev**: {df['volume'].std():.0f}
- **Min**: {df['volume'].min()}
- **Max**: {df['volume'].max()}

## Price Statistics

- **Mean**: {df['price'].mean():.0f} IDR
- **Median**: {df['price'].median():.0f} IDR
- **Min**: {df['price'].min()} IDR
- **Max**: {df['price'].max()} IDR

## Data Quality Checks

- ✅ No missing values: {df.isnull().sum().sum() == 0}
- ✅ All dates valid: {pd.to_datetime(df['date']).notna().all()}
- ✅ All volumes > 0: {(df['volume'] > 0).all()}
- ✅ All prices > 0: {(df['price'] > 0).all()}

## Usage

```python
import pandas as pd

# Load data
df = pd.read_csv("{data_file}")

# Train/val/test split (temporal)
df = df.sort_values('date')
train = df.iloc[:int(len(df)*0.6)]
val = df.iloc[int(len(df)*0.6):int(len(df)*0.8)]
test = df.iloc[int(len(df)*0.8):]

# Features
X = df[['volume', 'days_to_earnings', 'volume_zscore', 'day_of_week']]
y = df['is_suspicious']
```

---

**Ready for Phase 0 modeling!** 🚀
"""
        
        report_file.write_text(report, encoding='utf-8')
        logger.info(f"✅ Generated report: {report_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate synthetic transaction data')
    parser.add_argument(
        '--num-transactions',
        type=int,
        default=500,
        help='Total number of transactions to generate'
    )
    parser.add_argument(
        '--suspicious-ratio',
        type=float,
        default=0.2,
        help='Ratio of suspicious transactions (0.0-1.0)'
    )
    parser.add_argument(
        '--output-suffix',
        default='v1',
        help='Output file suffix'
    )
    
    args = parser.parse_args()
    
    # Validate
    if not 0 <= args.suspicious_ratio <= 1:
        raise ValueError("suspicious-ratio must be between 0 and 1")
    
    # Generate
    logger.info("🔄 Starting synthetic data generation...")
    generator = TransactionGenerator()
    
    df = generator.generate_dataset(
        num_transactions=args.num_transactions,
        suspicious_ratio=args.suspicious_ratio
    )
    
    filename = generator.save_dataset(df, suffix=args.output_suffix)
    
    logger.info("\n✅ Data generation complete!")
    logger.info(f"📊 Generated {len(df)} transactions")
    logger.info(f"📁 Saved to: {filename}")


if __name__ == "__main__":
    main()
