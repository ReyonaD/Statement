# Quick Start - Bank Statement Analyzer

## Installation (One Time)

```bash
# If on Ubuntu/Debian, install venv first:
sudo apt install python3-venv

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install pandas (venv must be activated)
pip install pandas
```

## Basic Usage

### 1. Add Your Statement Files
```bash
# Place CSV files in statements folder
cp ~/Downloads/bank-statement.csv statements/
```

### 2. Run Analysis
```bash
# Make sure venv is activated first!
source venv/bin/activate

python3 main.py
```

### 3. View Results
```bash
# Reports are in output folder
ls output/
open output/categories_summary.csv  # Mac
xdg-open output/categories_summary.csv  # Linux
```

## Common Tasks

### Test with Sample Data
```bash
python3 main.py
# Uses included sample-2025-01.csv
```

### Add New Category
Edit `rules.json`:
```json
{
  "name": "Uber Expense",
  "contains": ["uber", "lyft"],
  "type": "expense"
}
```

### Check What's Uncategorized
```bash
# After running main.py, check:
cat output/other_details.csv
```

### Process Specific Folder
```bash
python3 main.py /path/to/statements
```

## Output Files

- **categories_summary.csv** - Totals by category
- **monthly_summary.csv** - Monthly totals
- **monthly_detailed_summary.csv** - Monthly income/expense breakdown
- **other_details.csv** - Uncategorized transactions

## File Format

Your CSV should look like:
```
Date,Description,Amount,Running Balance
01/08/2025,SHOPIFY PAYMENTS,"2,408.66","52,408.66"
```

## Troubleshooting

**No transactions found**
- Check files are in `statements/` folder
- Ensure files are `.csv` or `.txt`

**Categories not matching**
- Check `rules.json` syntax
- Keywords are case-insensitive
- First matching rule wins

**pandas not installed**
```bash
pip install pandas
```

## More Help

- Full guide: [README.md](README.md)
- Setup: [SETUP.md](SETUP.md)
- Overview: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
