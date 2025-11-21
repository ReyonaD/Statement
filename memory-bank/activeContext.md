# Active Context

## Current Focus
Building MVP v1 - Bank Statement Analyzer with automated categorization and reporting.

## Recent Changes
- Created memory bank structure
- Defined project scope and requirements
- Planning implementation of core modules

## Next Steps
1. Create `rules.json` with categorization rules
2. Implement `parser.py` for statement loading
3. Implement `categorizer.py` for transaction categorization
4. Implement `reports.py` for summary generation
5. Create `main.py` CLI orchestrator
6. Write `README.md` with usage instructions
7. Create `requirements.txt`

## Active Decisions

### File Format Handling
- Starting with single format: comma-separated values in single column
- Format: Date, Description, Amount, Running Balance
- Handle quoted amounts with commas: `"1,234.56"`
- Split on first 3 commas only to preserve descriptions with commas

### Categorization Strategy
- Using JSON-based rules for flexibility
- Simple substring matching (case-insensitive)
- First match wins (rule order matters)
- Default to "Other" for unmatched transactions
- Rules include both category name and type (income/expense)

### Report Types
Three core reports identified:
1. Category summary - Overall spending by category
2. Monthly summary - Time-based trends
3. Other details - Uncategorized transaction breakdown for new pattern discovery

### Directory Structure
- `./statements/` - Input files
- `./output/` - Generated reports
- `./memory-bank/` - Project documentation
- Root level - Python modules and config

## Important Patterns

### DataFrame Column Naming
Standardize on lowercase with underscores:
- `date` (not Date or transaction_date)
- `description` (not Description)
- `amount` (not Amount or transaction_amount)
- `running_balance` (not Balance)
- `source_file` (added during parsing)
- `category` (added during categorization)

### Amount Convention
- Positive values = income/deposits
- Negative values = expenses/withdrawals
- This matches typical bank statement format

### Error Handling Philosophy
- Parser: Lenient - skip bad rows with warning
- Categorizer: Lenient - default to "Other"
- Reports: Lenient - handle empty data gracefully
- Config: Strict - fail fast if rules.json invalid

## Known Constraints

### Current Limitations
1. Single bank format only
2. All files must have same structure
3. No validation of balance calculations
4. No duplicate transaction detection
5. No manual category override mechanism
6. No date range filtering

### MVP Acceptable Trade-offs
- Memory-bound (must fit all transactions in RAM)
- Reprocess all files each run (no incremental updates)
- Simple string matching (no ML or fuzzy matching)
- No GUI (CLI only)

## Project Insights

### Why This Structure Works
- Separation of concerns makes testing easier
- JSON rules allow non-programmers to update categories
- Multiple report types serve different analysis needs
- File-based I/O keeps complexity low

### Critical Success Factors
1. Parser must handle quoted amounts correctly
2. Rules must be ordered (specific before general)
3. Reports must be readable in spreadsheet software
4. Error messages must be actionable

### Testing Strategy (Future)
- Unit tests for parser edge cases (quoted amounts, missing values)
- Unit tests for categorizer (matching logic, rule order)
- Integration test with sample statement files
- Validation that reports sum correctly

## Questions to Resolve
None currently - MVP scope is clear and well-defined.
