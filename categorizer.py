"""
Transaction categorization engine.

Applies rule-based categorization to transaction descriptions.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict


def load_rules(path: str) -> List[Dict]:
    """
    Load categorization rules from JSON file.

    Args:
        path: Path to rules.json file

    Returns:
        List of rule dictionaries with keys: name, contains, type

    Raises:
        FileNotFoundError: If rules file doesn't exist
        json.JSONDecodeError: If rules file is invalid JSON
    """
    rules_path = Path(path)

    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {path}")

    with open(rules_path, "r") as f:
        rules = json.load(f)

    # Validate rules structure
    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError(f"Rule {i} is not a dictionary")
        if "name" not in rule or "contains" not in rule:
            raise ValueError(f"Rule {i} missing required fields (name, contains)")
        if not isinstance(rule["contains"], list):
            raise ValueError(f"Rule {i} 'contains' must be a list")

    return rules


def apply_categories(df: pd.DataFrame, rules_path: str) -> pd.DataFrame:
    """
    Apply categorization rules to transactions.

    Args:
        df: DataFrame with transaction data (must have 'description' column)
        rules_path: Path to rules.json file

    Returns:
        DataFrame with added 'category' column

    Categorization logic:
        - First matching rule wins (rule order matters)
        - Case-insensitive substring matching
        - Unmatched transactions → "Other"
    """
    rules = load_rules(rules_path)

    def get_category(desc: str) -> str:
        """
        Determine category for a transaction description.

        Args:
            desc: Transaction description

        Returns:
            Category name
        """
        if pd.isna(desc) or desc == "":
            return "Other"

        desc_lower = desc.lower()

        # Check each rule in order
        for rule in rules:
            for keyword in rule["contains"]:
                if keyword.lower() in desc_lower:
                    return rule["name"]

        # No match found
        return "Other"

    # Apply categorization
    df = df.copy()
    df["category"] = df["description"].astype(str).apply(get_category)

    return df


def get_category_type(category: str, rules_path: str) -> str:
    """
    Get the type (income/expense) for a category.

    Args:
        category: Category name
        rules_path: Path to rules.json file

    Returns:
        "income", "expense", or "unknown"
    """
    rules = load_rules(rules_path)

    for rule in rules:
        if rule["name"] == category:
            return rule.get("type", "unknown")

    return "unknown"


if __name__ == "__main__":
    # Test the categorizer
    import sys

    # Create sample data
    sample_data = {
        "description": [
            "SHOPIFY PAYMENTS",
            "SHOPPAY INSTALLMENTS",
            "ZELLE TO JOHN DOE",
            "AMERICAN EXPRESS",
            "CAPITAL ONE PAYMENT",
            "DTF PRINTER USA LLC",
            "WIRE BOOK OUT",
            "TRANSFER FEE",
            "AMAZON MKTPL",
        ]
    }

    df = pd.DataFrame(sample_data)

    rules_file = sys.argv[1] if len(sys.argv) > 1 else "./rules.json"
    print(f"Loading rules from: {rules_file}\n")

    df_categorized = apply_categories(df, rules_file)

    print("Categorization test:")
    print(df_categorized[["description", "category"]])

    print("\nCategory counts:")
    print(df_categorized["category"].value_counts())
