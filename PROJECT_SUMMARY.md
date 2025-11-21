# Bank Statement Analyzer - Project Summary

## What You Have

A complete, working bank statement analysis system with:

### Core Modules ✓
- **parser.py** - Loads and normalizes CSV/TXT statement files
- **categorizer.py** - Applies rule-based transaction categorization
- **reports.py** - Generates 4 different summary reports
- **main.py** - Orchestrates the complete pipeline

### Configuration ✓
- **rules.json** - 8 pre-configured transaction categories
- **requirements.txt** - Python dependencies (pandas)

### Documentation ✓
- **README.md** - Complete user guide
- **SETUP.md** - Installation and quick start
- **memory-bank/** - Full project documentation (6 files)

### Sample Data ✓
- **statements/sample-2025-01.csv** - Example statement with 12 transactions

## How It Works

```
[Your Bank Statements]
         ↓
    parser.py          ← Loads & normalizes CSV files
         ↓
  categorizer.py       ← Applies rules.json patterns
         ↓
    reports.py         ← Generates 4 CSV reports
         ↓
   [Output Reports]
```

## Quick Start

```bash
# 1. Install dependencies
pip install pandas

# 2. Run with sample data
python3 main.py

# 3. Check output folder
ls output/
```

## Generated Reports

1. **categories_summary.csv**
   - Total and count by category
   - Shows: Shopify Income, AMEX Payment, Wire Transfer, etc.

2. **monthly_summary.csv**
   - Total amount by month
   - Format: YYYY-MM

3. **monthly_detailed_summary.csv**
   - Income, expense, net, and transaction count by month

4. **other_details.csv**
   - Breakdown of uncategorized transactions
   - Use to identify new patterns

## Pre-Configured Categories

**Income (2 categories):**
- Shopify Income
- Shop Pay / Affirm Income

**Expenses (6 categories):**
- Zelle Expense
- AMEX Payment
- Capital One Payment
- DTF Printer USA LLC Transfer
- Wire Transfer
- Bank Fee

**Default:**
- Other (unmatched transactions)

## Your Next Steps

### Option 1: Test with Sample Data
```bash
python3 main.py
# Check output/ folder for results
```

### Option 2: Use Your Own Data
1. Place your bank statement CSV files in `statements/`
2. Run: `python3 main.py`
3. Review reports in `output/`
4. Add new rules to `rules.json` for uncategorized items

### Option 3: Customize Categories
Edit `rules.json`:
```json
{
  "name": "Your Category",
  "contains": ["keyword1", "keyword2"],
  "type": "income"
}
```

## File Structure

```
Statement/
├── main.py                 ← Run this
├── parser.py               ← Statement loader
├── categorizer.py          ← Categorization engine
├── reports.py              ← Report generator
├── rules.json              ← Categories config
├── requirements.txt        ← Dependencies
├── README.md               ← User guide
├── SETUP.md                ← Installation guide
├── PROJECT_SUMMARY.md      ← This file
├── .gitignore              ← Git ignore
│
├── memory-bank/            ← Project documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── techContext.md
│   ├── systemPatterns.md
│   ├── activeContext.md
│   └── progress.md
│
├── statements/             ← INPUT: Place CSV files here
│   └── sample-2025-01.csv
│
└── output/                 ← OUTPUT: Reports appear here
    ├── categories_summary.csv
    ├── monthly_summary.csv
    ├── monthly_detailed_summary.csv
    └── other_details.csv
```

## Expected Input Format

Your bank statements should be CSV files with this format:

```csv
Date,Description,Amount,Running Balance
01/08/2025,SHOPIFY PAYMENTS,"2,408.66","52,408.66"
01/10/2025,ZELLE TO JOHN DOE,"-500.00","51,908.66"
```

**Key points:**
- Comma-separated values in single column
- Four fields: Date, Description, Amount, Balance
- Amounts can be quoted with commas: `"1,234.56"`
- Positive = income, Negative = expense

## Features

✅ Multi-file processing (process months of statements at once)
✅ Automatic categorization (rule-based matching)
✅ Multiple report types (category, monthly, detailed)
✅ CSV export (open in Excel/Sheets)
✅ Easy configuration (JSON rules)
✅ Handles quoted amounts with commas
✅ Date parsing (automatic)
✅ Source tracking (know which file each transaction came from)

## Testing Individual Components

```bash
# Test parser
python3 parser.py ./statements

# Test categorizer
python3 categorizer.py ./rules.json

# Test reports
python3 reports.py ./statements ./rules.json

# Run complete pipeline
python3 main.py
```

## Dependencies

Only one dependency:
- **pandas** >= 1.5.0 (data manipulation and CSV handling)

Install with:
```bash
pip install -r requirements.txt
```

## Memory Bank

Complete project documentation in `memory-bank/`:

- **projectbrief.md** - Project scope and goals
- **productContext.md** - Why it exists, how it works
- **techContext.md** - Technology stack and structure
- **systemPatterns.md** - Architecture and design decisions
- **activeContext.md** - Current focus and decisions
- **progress.md** - Status and evolution

These files help you (or AI assistants) understand the project architecture and make changes confidently.

## Support

- Check [README.md](README.md) for usage instructions
- Check [SETUP.md](SETUP.md) for installation help
- Review [memory-bank/](memory-bank/) for technical details
- Inspect sample data in [statements/sample-2025-01.csv](statements/sample-2025-01.csv)

## Success Criteria

You'll know it's working when:
1. ✓ `python3 main.py` runs without errors
2. ✓ Four CSV files appear in `output/`
3. ✓ Console shows summary statistics
4. ✓ Reports open correctly in spreadsheet software
5. ✓ Transactions are categorized correctly

## Made With

- Python 3.8+
- pandas (data processing)
- JSON (configuration)
- CSV (input/output)

---

**Ready to use!** Start with `python3 main.py` to test with sample data.
