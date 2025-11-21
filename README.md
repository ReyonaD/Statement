# Bank Statement Analyzer

Automated bank statement parser and categorizer with **interactive visual dashboard** and detailed reporting.

## 🎯 Two Ways to Use

### 🌐 Web App (Recommended) - NEW!
Interactive visual dashboard with filters, charts, and real-time exploration.

```bash
./run.sh
# Opens http://localhost:5000 in your browser
```

### 📊 CLI Tool
Command-line tool that generates CSV reports.

```bash
python main.py
# Outputs reports to output/ folder
```

## Features

### Web Application
- **Interactive Dashboard**: Visual cards, charts, and summaries
- **Powerful Filters**: Category, month, type, and text search
- **Drill Down**: Click any card to explore details
- **Real-Time**: Instant filtering and updates
- **Mobile Friendly**: Works on any device

### CLI Tool
- **Multi-File Processing**: Analyze multiple statement files at once
- **Automatic Categorization**: Rule-based transaction classification
- **Multiple Reports**: Category summaries, monthly trends, and detailed breakdowns
- **Easy Configuration**: Add categories via simple JSON file
- **CSV Export**: All reports exported as CSV for further analysis

## Quick Start

### 1. Installation

```bash
# Clone or download this project
cd Statement

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Add Your Statement Files

Place your bank statement files in the `statements/` folder:

```
statements/
  ├── 2025-07.csv
  ├── 2025-08.csv
  └── 2025-09.csv
```

**Expected file format:**
- CSV or TXT files
- Single column with comma-separated values
- Format: `Date,Description,Amount,Running Balance`
- Example: `01/08/2025,SHOPIFY PAYMENTS,"2,408.66","57,982.27"`

### 3. Run Analysis

```bash
python main.py
```

### 4. Review Reports

Check the `output/` folder for generated reports:

- **categories_summary.csv** - Total amount and count by category
- **monthly_summary.csv** - Monthly total amounts
- **monthly_detailed_summary.csv** - Monthly income/expense breakdown
- **other_details.csv** - Breakdown of uncategorized transactions

## Configuration

### Adding New Categories

Edit `rules.json` to add or modify categories:

```json
[
  {
    "name": "Shopify Income",
    "contains": ["shopify"],
    "type": "income"
  },
  {
    "name": "AMEX Payment",
    "contains": ["american express"],
    "type": "expense"
  }
]
```

**Rule structure:**
- `name`: Category display name
- `contains`: List of keywords to match (case-insensitive)
- `type`: "income" or "expense"

**Important:**
- Rules are checked in order (first match wins)
- Keywords are matched as substrings
- Put more specific rules before general ones

### Default Categories

The system comes pre-configured with these categories:

**Income:**
- Shopify Income
- Shop Pay / Affirm Income

**Expenses:**
- Zelle Expense
- AMEX Payment
- Capital One Payment
- DTF Printer USA LLC Transfer
- Wire Transfer
- Bank Fee

**Other:**
- Any transaction not matching rules

## Advanced Usage

### Custom Paths

```bash
# Specify custom folders
python main.py /path/to/statements /path/to/rules.json /path/to/output
```

### Testing Individual Modules

Test the parser:
```bash
python parser.py ./statements
```

Test the categorizer:
```bash
python categorizer.py ./rules.json
```

Test report generation:
```bash
python reports.py ./statements ./rules.json
```

## Reports Explained

### 1. Category Summary
Shows total and count for each category:
```
category,sum,count
Shopify Income,45678.90,23
AMEX Payment,-12345.67,5
...
```

### 2. Monthly Summary
Shows total amount by month:
```
month,total_amount
2025-07,15234.56
2025-08,18567.89
...
```

### 3. Monthly Detailed Summary
Shows income, expense, and net by month:
```
month,total_income,total_expense,net,transaction_count
2025-07,25000.00,-9765.44,15234.56,45
...
```

### 4. Other Details
Shows breakdown of uncategorized transactions:
```
description,sum,count
AMAZON MKTPL,-26.95,1
COSTCO WHSE,-156.78,3
...
```

Use this to identify patterns and create new rules.

## Troubleshooting

### No transactions found
- Verify files are in `statements/` folder
- Check file format (CSV or TXT)
- Ensure files contain comma-separated data

### Categories not matching
- Check `rules.json` syntax (valid JSON)
- Verify keywords are lowercase in rules
- Remember: first matching rule wins
- Check for typos in keywords

### Date parsing errors
- Dates should be in common formats (MM/DD/YYYY, etc.)
- Invalid dates will show as warnings but won't stop processing

### Missing dependencies
```bash
pip install -r requirements.txt
```

## Project Structure

```
Statement/
├── memory-bank/           # Project documentation
├── statements/            # Input: place CSV/TXT files here
├── output/                # Output: generated reports
├── rules.json             # Categorization rules
├── parser.py              # Statement file loader
├── categorizer.py         # Transaction categorization
├── reports.py             # Report generation
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Tips

1. **Review "Other" category** - Check `other_details.csv` regularly to find new patterns
2. **Order matters** - Put specific rules before general ones in `rules.json`
3. **Backup your rules** - Save `rules.json` when you've configured it
4. **Test incrementally** - Test with one file first, then add more
5. **Keep files organized** - Use consistent naming for statement files (e.g., YYYY-MM.csv)

## Future Enhancements

Potential improvements for future versions:
- Support for multiple bank formats
- Machine learning categorization
- Web interface
- Database storage
- Duplicate transaction detection
- Manual category override
- Budget tracking and alerts

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the memory bank documentation in `memory-bank/`
3. Verify your file formats match the expected structure

## License

Free to use and modify for personal or commercial purposes.
