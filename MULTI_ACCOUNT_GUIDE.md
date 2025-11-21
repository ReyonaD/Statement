# Multi-Account Bank Statement Analysis

## Overview

The app now supports analyzing **multiple bank accounts** simultaneously! You can view:
- **Combined view**: All accounts merged together
- **Individual view**: Each bank account separately

## How It Works

### Upload Multiple Files

Upload statement files from different bank accounts:

```
statements/
  ├── chase-checking-2025-07.csv     (Account 1)
  ├── chase-savings-2025-07.csv      (Account 2)
  ├── bofa-business-2025-07.csv      (Account 3)
  └── amex-2025-07.csv               (Account 4)
```

### View Combined (All Accounts)

By default, the dashboard shows **all accounts combined**:
- Total income across all accounts
- Total expenses across all accounts
- Net balance across all accounts

### Filter by Individual Account

Use the **"View by Bank Account"** dropdown at the top:

1. Select a specific file from the dropdown
2. Dashboard updates to show **only that account**
3. All charts, categories, and transactions filter automatically

## Features

### 1. Account Selection Dropdown

Located at the top of the dashboard:
- **All Accounts (Combined)** - Default view
- **filename.csv (N transactions)** - Each uploaded file

### 2. Automatic Filtering

When you select an account:
- ✅ Summary cards update (income, expense, net)
- ✅ Category breakdown shows only that account
- ✅ Monthly chart shows only that account
- ✅ Transaction list filters automatically

### 3. Transaction Filters

In the Transactions tab, you can filter by:
- **Bank Account** - Select specific file
- **Category** - Shopify, AMEX, etc.
- **Month** - Specific time period
- **Type** - Income/Expense
- **Search** - Text search

All filters work together!

## Use Cases

### Use Case 1: Personal + Business Accounts

Upload both accounts:
- `personal-checking.csv`
- `business-checking.csv`

**View combined**: See total household cash flow
**View separate**: Track business vs personal spending

### Use Case 2: Multiple Credit Cards

Upload all cards:
- `amex.csv`
- `chase-sapphire.csv`
- `capital-one.csv`

**View combined**: Total credit card spending
**View separate**: Which card has highest spending

### Use Case 3: Checking + Savings

Upload both:
- `checking-2025-07.csv`
- `savings-2025-07.csv`

**View combined**: Total account balances
**View separate**: Savings rate, checking activity

### Use Case 4: Multiple Months, Same Account

Upload monthly statements:
- `chase-2025-07.csv`
- `chase-2025-08.csv`
- `chase-2025-09.csv`

**View combined**: Quarter overview
**View separate**: Individual month analysis

## Examples

### Example 1: Filter Overview to One Account

```
1. Upload 3 bank statement files
2. Dashboard shows combined view (all 3 accounts)
3. Select "chase-checking.csv" from dropdown
4. See only Chase checking data
5. Income/expense/net update
6. Categories show only Chase transactions
```

### Example 2: Filter Transactions by Account + Category

```
1. Go to Transactions tab
2. Select "Bank Account: business-checking.csv"
3. Select "Category: Shopify Income"
4. See only Shopify income from business account
```

### Example 3: Compare Accounts

```
1. Select "Account A" - note total spending
2. Select "Account B" - note total spending
3. Compare which account has higher expenses
```

## Tips

### Organize Your Files

Use clear, consistent naming:
- ✅ `chase-checking-2025-07.csv`
- ✅ `bofa-business-2025-08.csv`
- ❌ `stmt.csv` (not descriptive)
- ❌ `download (1).csv` (confusing)

### Upload Strategy

**Option 1: All at once**
- Upload all accounts together
- Switch between them easily

**Option 2: One at a time**
- Upload one account
- Analyze it
- Delete and upload next

**Option 3: Keep all**
- Upload all and keep them
- Delete only when no longer needed

### Best Practices

1. **Name files clearly** - Include bank name and date
2. **Upload regularly** - Add new months as they come
3. **Use filters** - Combine account + category filters
4. **Check combined view** - See total household picture
5. **Drill into accounts** - Investigate specific accounts

## Technical Details

### How Files are Tracked

Each transaction has a `source_file` column:
```
Date,Description,Amount,Balance,Source File
01/08/2025,SHOPIFY,$100,$1000,chase-checking.csv
```

### Filtering Logic

When you select an account:
- Backend filters: `WHERE source_file = 'selected_file.csv'`
- All calculations run on filtered data
- No data from other files included

### Combined View

When "All Accounts" is selected:
- No filtering applied
- All transactions from all files included
- Totals sum across all accounts

## Troubleshooting

### "All accounts" shows unexpected data

Check uploaded files list:
- Go to Files tab
- See which files are uploaded
- Delete unwanted files

### Account not showing in dropdown

Refresh the page or:
- Click 🔄 Reload Data button
- Dropdown should update

### Transactions from wrong account

Make sure:
- Source file is correctly selected
- No other filters interfering
- File uploaded successfully

### Want to remove an account

Go to Files tab:
- Find the file
- Click 🗑️ Delete
- Data updates automatically

## Advanced Workflows

### Workflow 1: Monthly Review by Account

```bash
1. Upload all accounts for current month
2. Select each account one by one
3. Review categories per account
4. Check for unusual transactions
5. Export or take notes
```

### Workflow 2: Year-End Analysis

```bash
1. Upload all months for each account
2. View combined: Total year spending
3. View by account: Which account spent most
4. View by category: Where money went
```

### Workflow 3: Budget Tracking

```bash
1. Upload this month's statements
2. Select business account
3. Check "Expenses" category
4. Compare to budget
5. Repeat for personal account
```

## API Endpoints

For developers:

```
GET /api/summary?source_file=filename.csv
  - Get summary filtered by file

GET /api/transactions?source_file=filename.csv
  - Get transactions from specific file

GET /api/source-files
  - List all uploaded files with stats
```

## Summary

✅ **Upload multiple bank accounts**
✅ **View combined or separate**
✅ **Filter by account + category + month**
✅ **Compare accounts easily**
✅ **Manage files via web interface**

Now you can analyze all your bank accounts in one place! 🎉
