# Product Context

## Why This Exists
Managing business finances requires regular review of bank statements. Manual categorization of hundreds of transactions is tedious and error-prone. This tool automates the parsing and categorization process, providing clear insights into income sources and expense categories.

## Problems It Solves
1. **Time Waste**: Manual categorization of transactions takes hours each month
2. **Human Error**: Easy to miscategorize or miss transactions when doing manually
3. **Lack of Insights**: Hard to see spending patterns across multiple statement files
4. **Repetitive Work**: Same categorization logic applied month after month
5. **Data Entry**: No need to manually enter data into spreadsheets

## How It Works

### User Flow
1. User downloads statement files from bank (CSV format)
2. User places all files in `./statements/` directory
3. User runs `python main.py`
4. System processes all files and generates 3 CSV reports in `./output/`:
   - `categories_summary.csv` - Totals by category
   - `monthly_summary.csv` - Income/expense by month
   - `other_details.csv` - Breakdown of uncategorized transactions
5. User reviews reports in spreadsheet software or imports for further analysis

### Key Features
- **Automatic Categorization**: Rule-based system matches transaction descriptions to categories
- **Multi-File Processing**: Handles multiple statement files at once
- **Flexible Rules**: Easy to modify categorization via `rules.json`
- **Clear Reports**: Multiple views of the same data for different insights
- **Source Tracking**: Each transaction tagged with originating file

## User Experience Goals
- **Simple**: Drop files in folder, run one command
- **Fast**: Process months of statements in seconds
- **Transparent**: Easy to see which rules matched which transactions
- **Extensible**: Adding new categories should be trivial
- **Reliable**: Same input always produces same output

## Expected Categories
- **Income**:
  - Shopify Income
  - Shop Pay / Affirm Income

- **Expenses**:
  - Zelle Expense
  - AMEX Payment
  - Capital One Payment
  - DTF Printer USA LLC Transfer
  - Wire Transfer
  - Bank Fee

- **Uncategorized**:
  - Other (anything not matching rules)

## Report Use Cases
1. **Tax Prep**: Total income/expenses by category
2. **Budgeting**: Monthly spending trends
3. **Reconciliation**: Verify all transactions accounted for
4. **Investigation**: Drill into "Other" to find new patterns
5. **Forecasting**: Historical monthly patterns inform future planning
