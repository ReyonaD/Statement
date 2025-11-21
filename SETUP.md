# Setup Guide

## System Requirements
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Install System Dependencies (Ubuntu/Debian)

If you're on Ubuntu/Debian and get "externally-managed-environment" error:

```bash
# Install python3-venv package
sudo apt install python3.12-venv

# Or for general Python 3:
sudo apt install python3-venv
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows

# Your prompt should now show (venv)
```

### 3. Install Python Dependencies

```bash
# Make sure venv is activated (you should see "(venv)" in prompt)
pip install -r requirements.txt

# Or install pandas directly:
pip install pandas
```

### 4. Verify Installation

Test individual modules:

```bash
# Test the categorizer with sample data
python3 categorizer.py

# Test the parser with sample statement
python3 parser.py ./statements
```

### 5. Run Full Analysis

```bash
# Run with sample data (included)
python3 main.py

# Or run with your own data
# (place your .csv files in statements/ folder first)
python3 main.py
```

## Quick Test

A sample statement file is included at [statements/sample-2025-01.csv](statements/sample-2025-01.csv).

Run the analyzer:
```bash
python3 main.py
```

Expected output:
- Creates 4 CSV files in `output/` folder
- Prints summary statistics
- Shows categorization results

## Next Steps

1. **Add Your Real Data**:
   - Remove or replace `statements/sample-2025-01.csv`
   - Add your actual bank statement files to `statements/`

2. **Customize Categories**:
   - Edit [rules.json](rules.json) to add your transaction patterns
   - Test with `python3 categorizer.py`

3. **Review Reports**:
   - Open CSV files in `output/` with Excel, Google Sheets, or any spreadsheet software
   - Check `other_details.csv` to find new patterns for rules

## Troubleshooting

### pandas not found
```bash
pip install pandas
```

### No module named 'parser'
Make sure you're in the project directory:
```bash
cd /home/alp/Code/Statement
```

### Permission denied on main.py
Make it executable:
```bash
chmod +x main.py
```

### No files found
Make sure statement files are in `statements/` folder with `.csv` or `.txt` extension.

## File Locations

- **Input**: `statements/*.csv` or `statements/*.txt`
- **Output**: `output/*.csv`
- **Config**: `rules.json`
- **Code**: `parser.py`, `categorizer.py`, `reports.py`, `main.py`
- **Docs**: `memory-bank/*.md`
