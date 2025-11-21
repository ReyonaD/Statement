# Project Brief: Bank Statement Analyzer

## Overview
An automated bank statement parser and analyzer that processes multiple statement files, categorizes transactions, and generates financial reports.

## Core Problem
Manual processing of bank statements is time-consuming and error-prone. Need an automated way to:
- Parse multiple statement files from a directory
- Categorize transactions automatically
- Generate summary reports (category-based, monthly, counterparty-based)
- Export results for further analysis

## Target Users
Business owners and individuals who need to:
- Track income/expenses across multiple statements
- Understand spending patterns by category
- Generate reports for accounting/tax purposes
- Analyze transaction data over time

## MVP Scope
**In Scope:**
- Parse CSV/TXT bank statements with specific format (Date, Description, Amount, Balance)
- Rule-based transaction categorization (Shopify, Shop Pay, Zelle, AMEX, Wire, Fees, etc.)
- Generate reports:
  - Category summary (total, count, income/expense type)
  - Monthly summary (income, expense, net by month)
  - Counterparty details (especially for "Other" category)
- Export all reports as CSV
- Simple CLI interface

**Out of Scope (for MVP):**
- Multiple bank formats
- Machine learning categorization
- Database storage
- Web interface
- Manual category editing UI
- Multi-currency support

## Success Criteria
1. Successfully parses all statement files in `./statements/` directory
2. Categorizes transactions with >80% accuracy for known patterns
3. Generates 3 clear, usable CSV reports in `./output/`
4. Runs via simple CLI command: `python main.py`
5. Easy to add new categorization rules via `rules.json`

## Constraints
- Python-based (pandas for data processing)
- File-based input/output (no database)
- Single bank format support initially
- Must handle multi-month statement files
