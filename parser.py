"""
Bank statement file parser.

Loads CSV/TXT statement files and normalizes them into a standard DataFrame format.
"""

import pandas as pd
from pathlib import Path
import warnings


def load_all_statements(folder: str) -> pd.DataFrame:
    """
    Load all bank statement files from a folder and combine into single DataFrame.

    Args:
        folder: Path to folder containing statement files (*.csv, *.txt)

    Returns:
        DataFrame with columns: date, description, amount, running_balance, source_file

    Expected file format:
        - Single column with comma-separated values
        - Format: Date,Description,Amount,Running Balance
        - First row may contain headers/summaries (will be filtered)
        - Amounts may be quoted and contain commas: "1,234.56"
    """
    folder_path = Path(folder)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    # Collect all CSV and TXT files
    files = list(folder_path.glob("*.csv")) + list(folder_path.glob("*.txt"))

    if not files:
        warnings.warn(f"No CSV or TXT files found in {folder}")
        return pd.DataFrame(columns=["date", "description", "amount", "running_balance", "source_file"])

    all_dfs = []

    for file in files:
        try:
            df = _load_single_statement(file)
            all_dfs.append(df)
        except Exception as e:
            warnings.warn(f"Error loading {file.name}: {e}")
            continue

    if not all_dfs:
        warnings.warn("No files were successfully loaded")
        return pd.DataFrame(columns=["date", "description", "amount", "running_balance", "source_file"])

    # Combine all dataframes
    combined = pd.concat(all_dfs, ignore_index=True)

    # Convert date column to datetime
    combined["date"] = pd.to_datetime(combined["date"], errors="coerce")

    # Sort by date, then by sequence number to preserve CSV order within same date
    combined = combined.sort_values(["date", "_seq"]).reset_index(drop=True)

    return combined


def _load_single_statement(file_path: Path) -> pd.DataFrame:
    """
    Load a single statement file.

    Args:
        file_path: Path to statement file

    Returns:
        DataFrame with normalized transaction data
    """
    # Read first few lines to detect format
    with open(file_path, 'r') as f:
        first_lines = [f.readline() for _ in range(10)]

    # Check if this is a credit card statement (has "Posting Date" header)
    is_credit_card = any("Posting Date" in line for line in first_lines)

    if is_credit_card:
        df = _load_credit_card_statement(file_path)
    else:
        df = _load_csv_statement(file_path)

    # Add sequence number to preserve CSV order for transactions on the same date
    df['_seq'] = range(len(df))

    return df


def _load_csv_statement(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV-format bank statement (comma-separated).

    Format: Date,Description,Amount,Running Balance
    """
    import csv

    # Read CSV file properly handling quoted fields
    rows = []
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if len(row) >= 4:
                rows.append({
                    'date': row[0],
                    'description': row[1],
                    'amount': row[2],
                    'running_balance': row[3]
                })

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError(f"No valid rows found in {file_path.name}")

    # Skip first row (usually headers or summary)
    df = df.iloc[1:].copy()

    # Filter out rows where date column is empty or contains non-date text
    # Valid dates should be in MM/DD/YYYY format
    df["date"] = df["date"].str.strip()
    df = df[df["date"].str.len() > 0].copy()  # Remove empty dates

    # Filter out summary rows (like "Total credits", "Total debits")
    # These typically have keywords in the description
    # But keep "beginning balance" rows that have empty amount (they indicate starting balance)
    summary_keywords = ["total", "ending balance", "summary"]
    for keyword in summary_keywords:
        df = df[~df["description"].str.lower().str.contains(keyword, na=False)].copy()

    # Filter out "beginning balance" only if it has an amount (duplicate entry)
    # Keep it if amount is empty (it's a balance indicator)
    df = df[~((df["description"].str.lower().str.contains("beginning balance", na=False)) &
              (df["amount"].str.strip() != ""))].copy()

    # Clean and convert amount and balance
    # Remove quotes and convert to float
    df["amount"] = df["amount"].str.replace('"', '').str.strip()
    df["running_balance"] = df["running_balance"].str.replace('"', '').str.strip()

    # Remove commas from numbers (e.g., "1,234.56" -> "1234.56")
    df["amount"] = df["amount"].str.replace(',', '')
    df["running_balance"] = df["running_balance"].str.replace(',', '')

    # Convert to numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["running_balance"] = pd.to_numeric(df["running_balance"], errors="coerce")

    # Clean description (remove extra quotes, strip whitespace)
    df["description"] = df["description"].str.replace('"', '').str.strip()

    # Convert date before adding source_file
    # This allows us to filter out any rows that have invalid dates
    df["date_temp"] = pd.to_datetime(df["date"], errors="coerce")

    # Filter out rows where date couldn't be parsed
    df = df[df["date_temp"].notna()].copy()
    df["date"] = df["date_temp"]
    df = df.drop(columns=["date_temp"])

    # Add source file column
    df["source_file"] = file_path.name

    return df


def _load_credit_card_statement(file_path: Path) -> pd.DataFrame:
    """
    Load a credit card statement (fixed-width or tab-separated format).

    Format: Has columns including Posting Date, Description, Amount, Transaction Type (D/C)
    """
    # Read the file, skipping summary lines at the top
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find the header row (contains "Posting Date")
    header_idx = None
    for i, line in enumerate(lines):
        if "Posting Date" in line:
            header_idx = i
            break

    if header_idx is None:
        raise ValueError(f"Could not find header row in {file_path.name}")

    # Parse the header to find column positions
    header_line = lines[header_idx]
    import re

    # Find column positions in the header
    posting_date_pos = header_line.find("Posting Date")
    description_pos = header_line.find("Description")
    amount_pos = header_line.find("Amount")
    trans_type_pos = header_line.find("Transaction Type")

    transactions = []
    for line in lines[header_idx + 1:]:
        if not line.strip():
            continue

        try:
            # Split by multiple spaces (2+) to separate columns
            parts = re.split(r'\s{2,}', line.strip())

            if len(parts) < 6:  # Need at least cardholder, account, posting date, trans date, refid, description
                continue

            # Structure: [0]=Cardholder, [1]=Account#, [2]=Posting Date, [3]=Trans Date, [4]=Ref ID, [5]=Description, [6/7]=Amount, [...]=Type
            posting_date = None
            description = None
            amount = None
            trans_type = None

            # Find posting date (first MM/DD/YYYY after skipping cardholder name)
            for i, part in enumerate(parts):
                if i > 0 and re.match(r'^\d{2}/\d{2}/\d{4}$', part):
                    posting_date = part
                    # Description is typically 2-3 positions after posting date
                    # (skip Trans Date, possibly skip empty Ref ID)
                    for j in range(i + 2, min(i + 5, len(parts))):
                        candidate = parts[j].strip()
                        # Skip reference IDs (long numbers)
                        if re.match(r'^\d{10,}$', candidate):
                            continue
                        # Skip amounts
                        if re.match(r'^-?[\d,]+\.\d{2}$', candidate.replace(',', '')):
                            continue
                        # This looks like a description
                        if len(candidate) > 3:
                            description = candidate
                            break
                    break

            # Find amount (number with exactly 2 decimals, may have comma and minus sign)
            for part in parts:
                # Remove commas for matching
                clean_part = part.replace(',', '')
                if re.match(r'^-?\d+\.\d{2}$', clean_part):
                    amount = clean_part
                    break

            # Find transaction type (C or D) - usually near the end
            for part in parts:
                if part.strip() in ['C', 'D']:
                    trans_type = part.strip()
                    break

            # If we didn't find description at expected position, look for it
            if not description or len(description) < 3:
                for i, part in enumerate(parts):
                    part_clean = part.strip()
                    # Skip cardholder names, dates, numbers-only, and single chars
                    if i == 0:  # Skip cardholder
                        continue
                    if re.match(r'^\d+$', part_clean):  # Skip pure numbers
                        continue
                    if re.match(r'^\d{2}/\d{2}/\d{4}$', part_clean):  # Skip dates
                        continue
                    if re.match(r'^-?[\d,]+\.\d{2}$', part_clean):  # Skip amounts
                        continue
                    if len(part_clean) == 1:  # Skip single chars
                        continue
                    # This looks like a description
                    if len(part_clean) > 3:
                        description = part_clean
                        break

            if posting_date and description and amount:
                # For credit cards, we need to INVERT the sign:
                # Positive amount in file = charge/expense = need to make it NEGATIVE
                # Negative amount in file = payment/refund = need to make it POSITIVE
                # This way: negative = expense (red), positive = income (green)
                amount_float = -float(amount)  # Invert the sign

                transactions.append({
                    'date': posting_date,
                    'description': description.strip(),
                    'amount': amount_float,
                    'running_balance': None  # Credit cards don't have running balance
                })
        except (ValueError, IndexError) as e:
            continue

    if not transactions:
        raise ValueError(f"No valid transactions found in {file_path.name}")

    df = pd.DataFrame(transactions)
    df["source_file"] = file_path.name

    return df


if __name__ == "__main__":
    # Test the parser
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else "./statements"
    print(f"Loading statements from: {folder}")

    df = load_all_statements(folder)
    print(f"\nLoaded {len(df)} transactions from {df['source_file'].nunique()} files")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
