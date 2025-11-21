# 🚀 START HERE - Bank Statement Analyzer

## What You Have

A complete bank statement analysis system with:
- ✅ **Visual Web Dashboard** (interactive, filterable, charts)
- ✅ **CLI Tool** (generates CSV reports)
- ✅ **Your data ready**: `07ISAD stmt.csv` with 460+ transactions

## Quick Start (3 Steps)

### Step 1: Install Dependencies (One Time)

```bash
sudo apt install python3-venv
./setup.sh
```

### Step 2: Launch Web App

```bash
./run.sh
```

### Step 3: Open Browser

Go to: **http://localhost:5000**

That's it! 🎉

## What You'll See

### 📂 New! File Upload Tab

**No more manual file copying!**

1. Click the **📂 Files** tab
2. **Drag & drop** your CSV files directly
3. Or click **"Browse Files"** to select
4. Watch files upload with progress bar
5. Dashboard automatically refreshes!

**Features:**
- Drag & drop multiple files at once
- Real-time upload progress
- View all uploaded files
- Delete files with one click
- Auto-refresh after upload

See [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md) for details.

### Dashboard Features

#### 📊 Summary Cards
- Total Income, Total Expense, Net, Transaction Count
- Green = positive, Red = negative

#### 🏷️ Categories Tab
Click to see all your categories:
- Shopify Income
- Shop Pay / Affirm Income
- Zelle to JASA Apparel
- Zelle Expense
- AMEX Payment
- Capital One Payment
- Wire Transfer
- Bank Fee
- Other

#### 📝 Transactions Tab
**Powerful Filtering:**
- Filter by Category → See all Shopify transactions
- Filter by Month → See July, August, etc.
- Filter by Type → Income only or Expense only
- Search → Find specific descriptions

#### 📅 Monthly Tab
Month-by-month breakdown:
- Income per month
- Expenses per month
- Net per month
- Transaction count

### Interactive Features

**Click to Explore:**
- Click any category card → Shows filtered transactions
- Click "View Transactions" → Jumps to transaction list
- Click "View Details" on month → Shows month's transactions

**Real-Time Filters:**
- All filters update instantly
- Combine multiple filters
- Search while filtering

## Alternative: CLI Tool

If you prefer CSV exports:

```bash
source venv/bin/activate
python3 main.py
```

Generates 4 CSV files in `output/` folder:
- `categories_summary.csv`
- `monthly_summary.csv`
- `monthly_detailed_summary.csv`
- `other_details.csv`

## Your Data

✅ Already loaded: `statements/07ISAD stmt.csv`
- **460+ transactions** from July-October 2025
- Categories configured for your transaction types

### Add More Files

Just drop more CSV files in `statements/` folder, then click **🔄 Reload Data** in the web app.

## Customization

### Add New Categories

Edit `rules.json`:

```json
{
  "name": "Your Category",
  "contains": ["keyword1", "keyword2"],
  "type": "income"
}
```

**Important:** Put specific rules before general ones!

Example: "Zelle to JASA" is before generic "Zelle" so it matches first.

### Change Categories

Current categories already configured:
- ✅ Shopify Income
- ✅ Shop Pay / Affirm Income
- ✅ **Zelle to JASA Apparel** (separate from other Zelle)
- ✅ Zelle Expense (all other Zelle)
- ✅ AMEX Payment
- ✅ Capital One Payment
- ✅ Wire Transfer
- ✅ Bank Fee

## Troubleshooting

### "No module named 'flask'"
```bash
source venv/bin/activate
pip install flask
```

### "Port 5000 already in use"
Edit `app.py`, change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### "Virtual environment not found"
```bash
./setup.sh
```

### Web page is blank
Check browser console (F12) for errors, or check terminal for server errors.

## File Structure

```
Statement/
├── run.sh              ← Launch web app
├── setup.sh            ← One-time setup
├── app.py              ← Web server
├── main.py             ← CLI tool
├── rules.json          ← Your categories
│
├── statements/         ← Your CSV files
│   └── 07ISAD stmt.csv
│
├── output/             ← CLI reports appear here
│
├── templates/          ← Web UI
│   └── index.html
│
└── static/             ← Styles & JavaScript
    ├── css/style.css
    └── js/app.js
```

## Documentation

- **[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)** - Detailed web app features
- **[README.md](README.md)** - Complete user manual
- **[QUICK_START.md](QUICK_START.md)** - CLI quick reference
- **[INSTALL.md](INSTALL.md)** - Installation help

## Tips

1. **Start with Web App** - It's visual and interactive
2. **Use CLI for Exports** - When you need CSV files for Excel
3. **Check "Other" Category** - Find new patterns to categorize
4. **Bookmark Filters** - Browser back/forward works
5. **Mobile Works** - Open on phone/tablet

## What to Do Now

1. **Run it**: `./run.sh`
2. **Explore**: Click around, try filters
3. **Check "Other"**: See what's uncategorized
4. **Add rules**: Update `rules.json` for new patterns
5. **Reload**: Click 🔄 button to refresh

## Success!

You now have a professional bank statement analyzer with:
- ✅ Visual dashboard
- ✅ Real-time filtering
- ✅ CSV export capability
- ✅ Your data already loaded
- ✅ Categories pre-configured

**Run `./run.sh` and open http://localhost:5000 to get started!**

---

Questions? Check [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) for detailed features.
