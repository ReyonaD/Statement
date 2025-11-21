#!/usr/bin/env python3
"""
Bank Statement Analyzer - Main CLI Entry Point

Orchestrates the complete pipeline:
1. Load statement files from ./statements/
2. Apply categorization rules from ./rules.json
3. Generate summary reports to ./output/

Usage:
    python main.py [statements_folder] [rules_file] [output_folder]

Defaults:
    statements_folder: ./statements
    rules_file: ./rules.json
    output_folder: ./output
"""

import sys
from pathlib import Path

from parser import load_all_statements
from categorizer import apply_categories
from reports import (
    save_category_summary,
    save_other_details,
    save_monthly_summary,
    save_detailed_monthly_summary,
    print_summary_stats
)


def main():
    """
    Main entry point for bank statement analyzer.
    """
    # Parse command line arguments
    statements_folder = sys.argv[1] if len(sys.argv) > 1 else "./statements"
    rules_file = sys.argv[2] if len(sys.argv) > 2 else "./rules.json"
    output_folder = sys.argv[3] if len(sys.argv) > 3 else "./output"

    print("="*60)
    print("BANK STATEMENT ANALYZER")
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  Statements folder: {statements_folder}")
    print(f"  Rules file:        {rules_file}")
    print(f"  Output folder:     {output_folder}")
    print()

    # Validate inputs
    if not Path(statements_folder).exists():
        print(f"ERROR: Statements folder not found: {statements_folder}")
        print(f"Please create the folder and add your bank statement files (.csv or .txt)")
        sys.exit(1)

    if not Path(rules_file).exists():
        print(f"ERROR: Rules file not found: {rules_file}")
        print(f"Please ensure rules.json exists in the current directory")
        sys.exit(1)

    try:
        # Step 1: Load statements
        print("Step 1: Loading bank statements...")
        df = load_all_statements(statements_folder)

        if df.empty:
            print("ERROR: No transactions found in statement files")
            sys.exit(1)

        print(f"✓ Loaded {len(df):,} transactions from {df['source_file'].nunique()} file(s)")

        # Step 2: Apply categorization
        print("\nStep 2: Applying categorization rules...")
        df = apply_categories(df, rules_file)

        category_counts = df["category"].value_counts()
        print(f"✓ Categorized into {len(category_counts)} categories")

        # Step 3: Generate reports
        print(f"\nStep 3: Generating reports to {output_folder}/...")
        save_category_summary(df, output_folder)
        save_other_details(df, output_folder)
        save_monthly_summary(df, output_folder)
        save_detailed_monthly_summary(df, output_folder)

        # Print summary statistics
        print_summary_stats(df)

        print("SUCCESS: All reports generated successfully!")
        print(f"\nNext steps:")
        print(f"  1. Review reports in: {output_folder}/")
        print(f"  2. Check 'Other' category in other_details.csv")
        print(f"  3. Add new rules to {rules_file} if needed")
        print()

    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
