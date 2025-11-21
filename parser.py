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

    # Sort by date
    combined = combined.sort_values("date").reset_index(drop=True)

    return combined


def _load_single_statement(file_path: Path) -> pd.DataFrame:
    """
    Load a single statement file.

    Args:
        file_path: Path to statement file

    Returns:
        DataFrame with normalized transaction data
    """
    # Read file as single column (tab-separated to avoid splitting on commas)
    df_raw = pd.read_csv(file_path, sep="\t", header=None, engine="python")

    # Split the single column by comma (max 3 splits to preserve commas in description)
    df_split = df_raw[0].str.split(",", n=3, expand=True)

    # Filter to rows with all 4 columns
    df = df_split[df_split[3].notna()].copy()

    if df.empty:
        raise ValueError(f"No valid 4-column rows found in {file_path.name}")

    # Skip first row (usually headers or summary)
    df = df.iloc[1:].copy()

    # Name columns
    df.columns = ["date", "description", "amount", "running_balance"]

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

    # Add source file column
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
