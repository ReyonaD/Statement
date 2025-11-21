# Technical Context

## Technology Stack
- **Language**: Python 3.8+
- **Core Library**: pandas (data manipulation and analysis)
- **File Format**: CSV/TXT input, CSV output
- **Configuration**: JSON (for categorization rules)

## Dependencies
```
pandas>=1.5.0
```

## Project Structure
```
project_root/
├── memory-bank/          # Project documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── techContext.md
│   ├── systemPatterns.md
│   ├── activeContext.md
│   └── progress.md
├── statements/           # Input: bank statement files (.csv)
├── output/               # Output: generated reports (.csv)
├── rules.json            # Categorization rules configuration
├── parser.py             # File loading and normalization
├── categorizer.py        # Transaction categorization logic
├── reports.py            # Report generation functions
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
└── README.md             # User documentation
```

## Input File Format
Bank statements expected in CSV format with specific structure:
- Single column containing comma-separated values
- Format: `Date,Description,Amount,Running Balance`
- May contain header/summary rows (will be filtered)
- Amount format: Quoted strings with decimals (e.g., "1234.56")
- Dates: Various formats, parsed automatically

Example raw line:
```
01/08/2025,SHOPIFY PAYMENTS,"2,408.66","57,982.27"
```

## Output Files
1. **categories_summary.csv**
   - Columns: category, sum, count
   - One row per category
   - Shows total amount and transaction count

2. **monthly_summary.csv**
   - Columns: month, total_amount
   - One row per month
   - Month format: YYYY-MM

3. **other_details.csv**
   - Columns: description, sum, count
   - One row per unique description in "Other" category
   - Helps identify patterns for new rules

## Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the analyzer
python main.py
```

## Technical Constraints
1. **File Size**: Limited by available memory (pandas loads entire dataset)
2. **Format Support**: Only one bank format supported initially
3. **Date Parsing**: Relies on pandas automatic parsing (may fail on unusual formats)
4. **Text Encoding**: Assumes UTF-8 or ASCII
5. **Performance**: Not optimized for very large datasets (100k+ transactions)

## Error Handling Strategy
- Malformed lines: Skip with warning
- Parse errors: Convert to NaN, continue processing
- Missing files: Clear error message
- Invalid rules: Fail fast on startup

## Future Technical Considerations
- Support for multiple bank formats (abstraction layer)
- Database storage for historical data
- Incremental processing (avoid reprocessing same files)
- Configuration file for file path settings
- Logging system for debugging
- Unit tests for parser and categorizer
