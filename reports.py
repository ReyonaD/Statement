"""
Report generation module.

Generates summary reports from categorized transaction data.
"""

import pandas as pd
from pathlib import Path


def save_category_summary(df: pd.DataFrame, out_folder: str) -> pd.DataFrame:
    """
    Generate and save category summary report.

    Args:
        df: Categorized transaction DataFrame
        out_folder: Output directory path

    Returns:
        Summary DataFrame (also saved to CSV)

    Output columns:
        - category: Category name
        - sum: Total amount for category
        - count: Number of transactions
    """
    Path(out_folder).mkdir(exist_ok=True, parents=True)

    # Group by category and aggregate
    summary = df.groupby("category")["amount"].agg(["sum", "count"]).reset_index()

    # Sort by absolute sum (largest first)
    summary = summary.sort_values("sum", key=abs, ascending=False)

    # Save to CSV
    output_path = Path(out_folder) / "categories_summary.csv"
    summary.to_csv(output_path, index=False)
    print(f"✓ Category summary saved to: {output_path}")

    return summary


def save_other_details(df: pd.DataFrame, out_folder: str) -> pd.DataFrame:
    """
    Generate and save detailed breakdown of "Other" category transactions.

    Args:
        df: Categorized transaction DataFrame
        out_folder: Output directory path

    Returns:
        Details DataFrame (also saved to CSV)

    Output columns:
        - description: Transaction description
        - sum: Total amount for this description
        - count: Number of transactions with this description
    """
    Path(out_folder).mkdir(exist_ok=True, parents=True)

    # Filter to "Other" category
    other = df[df["category"] == "Other"]

    if other.empty:
        print("✓ No 'Other' transactions found")
        # Create empty file anyway
        empty_df = pd.DataFrame(columns=["description", "sum", "count"])
        output_path = Path(out_folder) / "other_details.csv"
        empty_df.to_csv(output_path, index=False)
        return empty_df

    # Group by description
    by_desc = other.groupby("description")["amount"].agg(["sum", "count"]).reset_index()

    # Sort by absolute sum (largest first)
    by_desc = by_desc.sort_values("sum", key=abs, ascending=False)

    # Save to CSV
    output_path = Path(out_folder) / "other_details.csv"
    by_desc.to_csv(output_path, index=False)
    print(f"✓ Other category details saved to: {output_path}")

    return by_desc


def save_monthly_summary(df: pd.DataFrame, out_folder: str) -> pd.DataFrame:
    """
    Generate and save monthly summary report.

    Args:
        df: Categorized transaction DataFrame
        out_folder: Output directory path

    Returns:
        Monthly summary DataFrame (also saved to CSV)

    Output columns:
        - month: Month in YYYY-MM format
        - total_amount: Sum of all transactions for the month
    """
    Path(out_folder).mkdir(exist_ok=True, parents=True)

    # Add month column
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Group by month
    monthly = df.groupby("month")["amount"].agg(
        total_amount="sum"
    ).reset_index()

    # Sort by month
    monthly = monthly.sort_values("month")

    # Save to CSV
    output_path = Path(out_folder) / "monthly_summary.csv"
    monthly.to_csv(output_path, index=False)
    print(f"✓ Monthly summary saved to: {output_path}")

    return monthly


def save_detailed_monthly_summary(df: pd.DataFrame, out_folder: str) -> pd.DataFrame:
    """
    Generate and save detailed monthly summary with income/expense breakdown.

    Args:
        df: Categorized transaction DataFrame
        out_folder: Output directory path

    Returns:
        Detailed monthly summary DataFrame (also saved to CSV)

    Output columns:
        - month: Month in YYYY-MM format
        - total_income: Sum of positive amounts
        - total_expense: Sum of negative amounts
        - net: Income + Expense
        - transaction_count: Number of transactions
    """
    Path(out_folder).mkdir(exist_ok=True, parents=True)

    # Add month column
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Calculate income and expense separately
    monthly = df.groupby("month").agg(
        total_income=("amount", lambda x: x[x > 0].sum()),
        total_expense=("amount", lambda x: x[x < 0].sum()),
        transaction_count=("amount", "count")
    ).reset_index()

    # Calculate net
    monthly["net"] = monthly["total_income"] + monthly["total_expense"]

    # Sort by month
    monthly = monthly.sort_values("month")

    # Save to CSV
    output_path = Path(out_folder) / "monthly_detailed_summary.csv"
    monthly.to_csv(output_path, index=False)
    print(f"✓ Detailed monthly summary saved to: {output_path}")

    return monthly


def print_summary_stats(df: pd.DataFrame) -> None:
    """
    Print high-level summary statistics to console.

    Args:
        df: Categorized transaction DataFrame
    """
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)

    # Overall stats
    total_transactions = len(df)
    total_income = df[df["amount"] > 0]["amount"].sum()
    total_expense = df[df["amount"] < 0]["amount"].sum()
    net = total_income + total_expense

    print(f"\nTotal Transactions: {total_transactions:,}")
    print(f"Total Income:       ${total_income:,.2f}")
    print(f"Total Expense:      ${total_expense:,.2f}")
    print(f"Net:                ${net:,.2f}")

    # Date range
    if not df["date"].isna().all():
        date_min = df["date"].min()
        date_max = df["date"].max()
        print(f"\nDate Range: {date_min.strftime('%Y-%m-%d')} to {date_max.strftime('%Y-%m-%d')}")

    # Top categories
    print("\nTop 5 Categories by Absolute Amount:")
    top_cats = df.groupby("category")["amount"].sum().abs().sort_values(ascending=False).head()
    for cat, amt in top_cats.items():
        actual_amt = df[df["category"] == cat]["amount"].sum()
        print(f"  {cat:30s} ${actual_amt:>12,.2f}")

    print("="*60 + "\n")


if __name__ == "__main__":
    # Test the reports module
    import sys
    from parser import load_all_statements
    from categorizer import apply_categories

    statements_folder = sys.argv[1] if len(sys.argv) > 1 else "./statements"
    rules_file = sys.argv[2] if len(sys.argv) > 2 else "./rules.json"
    output_folder = "./output"

    print(f"Loading statements from: {statements_folder}")
    df = load_all_statements(statements_folder)

    print(f"Applying categories from: {rules_file}")
    df = apply_categories(df, rules_file)

    print(f"\nGenerating reports to: {output_folder}")
    save_category_summary(df, output_folder)
    save_other_details(df, output_folder)
    save_monthly_summary(df, output_folder)
    save_detailed_monthly_summary(df, output_folder)

    print_summary_stats(df)
