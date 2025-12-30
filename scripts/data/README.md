# Data Collection Scripts - Usage Guide

## 📁 Scripts Created

### 1. News Scraper (`scrape_news.py`)

Scrape Indonesian financial news articles about insider trading.

### 2. Synthetic Data Generator (`generate_synthetic.py`)

Generate realistic synthetic transaction data for testing.

---

## 🚀 Quick Start

### Install Dependencies

```bash
# Activate environment
.\venv\Scripts\Activate.ps1

# Install scraping dependencies
pip install beautifulsoup4 requests Faker lxml
```

---

## 📰 News Scraper Usage

### Basic Usage

```bash
# Scrape from Kontan (default)
python scripts/data/scrape_news.py

# Scrape 100 articles
python scripts/data/scrape_news.py --max-articles 100

# Scrape from all sources
python scripts/data/scrape_news.py --source all --max-articles 500

# Custom keywords
python scripts/data/scrape_news.py --keywords "insider trading" "transaksi afiliasi" --max-articles 200
```

### Options

- `--source`: News source (`kontan`, `cnbc`, `bisnis`, `all`)
- `--max-articles`: Maximum articles per keyword (default: 100)
- `--keywords`: Search keywords (default: insider trading terms)

### Output

```
data/raw/news/
├── kontan_articles_20241229_032610.csv
├── cnbc_articles_20241229_033015.csv
└── bisnis_articles_20241229_033420.csv
```

---

## 🎲 Synthetic Data Generator Usage

### Basic Usage

```bash
# Generate 500 transactions (default)
python scripts/data/generate_synthetic.py

# Generate 1000 transactions
python scripts/data/generate_synthetic.py --num-transactions 1000

# 30% suspicious transactions
python scripts/data/generate_synthetic.py --suspicious-ratio 0.3

# Custom output
python scripts/data/generate_synthetic.py --output-suffix v2
```

### Options

- `--num-transactions`: Total transactions (default: 500)
- `--suspicious-ratio`: Ratio of suspicious (default: 0.2 = 20%)
- `--output-suffix`: Output file suffix (default: v1)

### Output

```
data/raw/transactions/
├── synthetic_transactions_v1_20241229_032610.csv
└── DATA_REPORT_synthetic_transactions_v1_20241229_032610.md
```

### Generated Features

- `transaction_id`: Unique identifier
- `date`: Transaction date
- `company`: Ticker symbol (BBCA, BBRI, etc.)
- `insider_name`: Person name
- `insider_role`: Director, Commissioner, etc.
- `action`: BUY or SELL
- `volume`: Number of shares
- `price`: Price per share (IDR)
- `total_value`: Total transaction value
- `days_to_earnings`: Days until earnings announcement
- `is_suspicious`: True/False label
- `violation_type`: Type of violation (if suspicious)
- `reason`: Explanation
- **Derived features**: `volume_zscore`, `day_of_week`, `month`, etc.

---

## 📊 Example Workflow

### Step 1: Generate Synthetic Data (Start Here!)

```bash
# Generate 500 transactions for testing
python scripts/data/generate_synthetic.py --num-transactions 500

# Check output
ls data/raw/transactions/
```

**Why start here?**

- ✅ No internet required
- ✅ Instant results (5 seconds)
- ✅ Perfect for testing RAG pipeline
- ✅ Includes ground truth labels

### Step 2: Scrape News (Optional)

```bash
# Scrape 100 articles from Kontan
python scripts/data/scrape_news.py --source kontan --max-articles 100
```

**Note**: Web scraping may require:

- Adjusting CSS selectors (sites change)
- Respecting rate limits
- Handling anti-bot measures

### Step 3: Use in RAG Pipeline

```python
# In Jupyter notebook
import pandas as pd

# Load synthetic data
df = pd.read_csv('data/raw/transactions/synthetic_transactions_v1_*.csv')

# Load news (if scraped)
news = pd.read_csv('data/raw/news/kontan_articles_*.csv')

# Use in RAG pipeline
# See: notebooks/1.1-quickstart-demo.ipynb
```

---

## 🎯 Phase 0 Checklist

### Week 1 Tasks

- [x] Create scraper scripts ✅
- [ ] **Generate 500 synthetic transactions** ← DO THIS FIRST
- [ ] Scrape 100-500 news articles
- [ ] Collect 10-20 POJK PDFs (manual download)
- [ ] Build RAG proof of concept

### Commands to Run

```bash
# 1. Generate data (5 seconds)
python scripts/data/generate_synthetic.py

# 2. Scrape news (10-30 minutes)  
python scripts/data/scrape_news.py --max-articles 100

# 3. Check outputs
ls data/raw/transactions/
ls data/raw/news/
```

---

## ⚠️ Important Notes

### News Scraper Limitations

1. **Site Structure**: Scrapers use CSS selectors that may break if sites update
2. **Rate Limiting**: Be polite - script includes delays (1-3 sec between requests)
3. **Robots.txt**: Respect each site's `robots.txt` policies
4. **Manual Review**: Some sites may require manual tweaking

### Recommendations

- **Start with synthetic data** - it's ready to use immediately
- **Test scrapers** on small batches first (`--max-articles 10`)
- **Manual collection** for POJK PDFs is more reliable

---

## 🐛 Troubleshooting

### Error: "Module not found"

```bash
pip install beautifulsoup4 requests Faker lxml
```

### Error: "No articles scraped"

- Site structure may have changed
- Check internet connection
- Try manual scraping from browser first

### Slow Performance

- Reduce `--max-articles`
- Scrape one source at a time
- Check network speed

---

## 📈 Next Steps

After generating data:

1. **Review Output**

   ```bash
   # Open generated CSV
   # Check data quality report
   ```

2. **Use in RAG POC**
   - Open Jupyter Lab
   - Load data in notebook
   - Test Q&A with Llama 3.1

3. **Document Sources**
   - Update `data/raw/README.md`
   - Track data provenance

---

## 🎉 Quick Win

**Generate data RIGHT NOW (5 seconds)**:

```bash
.\venv\Scripts\Activate.ps1
python scripts/data/generate_synthetic.py
```

You'll have 500 labeled transactions ready for Phase 0! 🚀
