# System Patterns

## Architecture Overview
Simple pipeline architecture with three main stages:
1. **Parse**: Load and normalize raw statement files
2. **Categorize**: Apply rules to classify transactions
3. **Report**: Generate summary views and export

```
[statements/*.csv]
    → parser.py → [DataFrame]
    → categorizer.py → [Categorized DataFrame]
    → reports.py → [output/*.csv]
```

## Key Design Decisions

### 1. Rule-Based Categorization (vs ML)
**Decision**: Use simple substring matching rules in JSON config
**Rationale**:
- MVP needs speed and simplicity
- Patterns are well-defined and stable
- Easy for non-technical users to modify
- Deterministic and debuggable
**Trade-off**: Less flexible than ML, requires manual rule updates

### 2. pandas DataFrame as Core Data Structure
**Decision**: Use pandas throughout the pipeline
**Rationale**:
- Native CSV reading/writing
- Powerful groupby and aggregation
- Date/time handling built-in
- Familiar to Python data analysts
**Trade-off**: Higher memory usage, not suitable for streaming very large files

### 3. File-Based I/O (vs Database)
**Decision**: Read from files, write to files, no persistence
**Rationale**:
- MVP simplicity
- Easy to inspect inputs/outputs
- No database setup required
- Portable across systems
**Trade-off**: No incremental processing, must reprocess all files each run

### 4. Modular File Structure
**Decision**: Separate files for parser, categorizer, reports, main
**Rationale**:
- Clear separation of concerns
- Easy to test individual components
- Easy to extend (e.g., new report types)
- Readable and maintainable

## Component Relationships

### parser.py
**Responsibility**: Load raw files → clean DataFrame
**Input**: Folder path (string)
**Output**: DataFrame with columns: date, description, amount, running_balance, source_file
**Key Functions**:
- `load_all_statements(folder: str) -> pd.DataFrame`
- Handles: File iteration, CSV parsing, data type conversion, column naming

### categorizer.py
**Responsibility**: DataFrame → Categorized DataFrame
**Input**: DataFrame + rules file path
**Output**: Same DataFrame with added 'category' column
**Key Functions**:
- `load_rules(path: str) -> list[dict]`
- `apply_categories(df: pd.DataFrame, rules_path: str) -> pd.DataFrame`
- Handles: Rule loading, substring matching, default category assignment

### reports.py
**Responsibility**: Categorized DataFrame → CSV reports
**Input**: Categorized DataFrame + output folder
**Output**: CSV files written to disk
**Key Functions**:
- `save_category_summary(df, out_folder) -> pd.DataFrame`
- `save_other_details(df, out_folder) -> pd.DataFrame`
- `save_monthly_summary(df, out_folder) -> pd.DataFrame`
- Handles: Grouping, aggregation, file writing

### main.py
**Responsibility**: Orchestrate the pipeline
**Input**: None (uses hardcoded paths)
**Output**: Console messages + files
**Key Functions**:
- `main()`: Coordinates parser → categorizer → reports
- Handles: High-level flow, error messages

## Data Flow

### Transaction DataFrame Schema
```python
{
    'date': datetime64,           # Transaction date
    'description': str,           # Transaction description
    'amount': float,              # Transaction amount (+ income, - expense)
    'running_balance': float,     # Account balance after transaction
    'source_file': str,           # Originating file name
    'category': str,              # Applied category (added by categorizer)
    'month': Period,              # YYYY-MM (added by monthly report)
}
```

### Rules Configuration Schema
```json
[
  {
    "name": "Category Name",
    "contains": ["keyword1", "keyword2"],
    "type": "income" | "expense"
  }
]
```

## Categorization Algorithm
```python
For each transaction:
    description_lower = description.lower()

    For each rule in rules:
        For each keyword in rule.contains:
            If keyword.lower() in description_lower:
                category = rule.name
                break

    If no match:
        category = "Other"
```

**Characteristics**:
- First match wins (order matters in rules.json)
- Case-insensitive matching
- Substring match (not whole word)
- No regex support in MVP

## Critical Implementation Paths

### Path 1: File Parsing
```
CSV file → pd.read_csv with tab separator →
split first column by comma →
filter valid rows (4 columns) →
remove header row →
rename columns →
convert types (amount, balance to float, date to datetime) →
add source_file column →
combine all files
```

**Edge Cases**:
- Amount with quotes: `"1,234.56"` → remove quotes, convert to float
- Missing balance: Set to NaN, continue
- Malformed date: Set to NaT, continue
- Extra commas in description: Only split on first 3 commas (n=3)

### Path 2: Categorization
```
Load rules.json →
For each row in DataFrame →
Apply categorization function →
Add category column
```

**Edge Cases**:
- Empty description: Category = "Other"
- Multiple matching rules: First rule wins
- Invalid rules.json: Fail with clear error

### Path 3: Report Generation
```
Categorized DataFrame →
groupby(category/month/description) →
aggregate(sum, count) →
to_csv()
```

**Edge Cases**:
- No transactions: Empty DataFrame, write empty CSV
- Missing output directory: Create it
- File write permission error: Fail with error message

## Error Handling Patterns

### Parse Errors
- Log warning, skip row, continue
- Example: `Warning: Could not parse line 42 in file 2025-07.csv`

### Configuration Errors
- Fail fast on startup
- Example: `Error: rules.json not found or invalid`

### I/O Errors
- Clear error message with path
- Example: `Error: Cannot write to ./output (permission denied)`

## Extension Points
1. **New Bank Formats**: Create new parser module, abstract interface
2. **New Categories**: Update rules.json
3. **New Reports**: Add function to reports.py, call from main.py
4. **Custom Filters**: Add filter parameter to report functions
5. **Output Formats**: Add new export functions (JSON, Excel, etc.)
