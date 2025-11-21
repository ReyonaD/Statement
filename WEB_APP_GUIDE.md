# Web Application Guide

## Visual Bank Statement Analyzer

An interactive web-based dashboard for exploring your bank transactions with filters, charts, and detailed views.

## Features

### 📊 Dashboard Overview
- **Summary Cards**: Total income, expenses, net, and transaction count
- **Category Grid**: Visual cards for each category with totals
- **Monthly Chart**: Bar chart showing monthly trends
- **Interactive**: Click any card to filter and drill down

### 📁 Categories View
- Detailed breakdown of each category
- Total, count, and average per category
- Click to view all transactions in that category

### 📝 Transactions View
- Full transaction list with powerful filters:
  - Filter by category
  - Filter by month
  - Filter by type (income/expense)
  - Search by description
- Paginated results (50 per page)
- Click category to filter transactions

### 📅 Monthly View
- Month-by-month breakdown
- Income, expense, and net for each month
- Transaction count per month
- Click to view month's transactions

## Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Install Flask
pip install -r requirements.txt
```

### 2. Run the Web App

```bash
python3 app.py
```

You'll see:
```
============================================================
Bank Statement Analyzer - Web Application
============================================================

Loading data...
✓ Loaded XXX transactions

Starting web server...

🌐 Open your browser to: http://localhost:5000

Press Ctrl+C to stop the server
============================================================
```

### 3. Open in Browser

Go to: **http://localhost:5000**

## How to Use

### Navigate Between Tabs
- **Overview**: High-level summary and charts
- **Categories**: Detailed category breakdown
- **Transactions**: Searchable, filterable transaction list
- **Monthly**: Month-by-month analysis

### Filter Transactions
1. Click the **Transactions** tab
2. Use the filter dropdowns:
   - Select a category
   - Select a month
   - Choose income/expense/all
   - Type in search box
3. Results update automatically

### Drill Down
- **From Overview**: Click any category card → jumps to filtered transactions
- **From Categories**: Click "View Transactions" → shows category transactions
- **From Monthly**: Click "View Details" → shows month's transactions

### Reload Data
Click the **🔄 Reload Data** button in the header to refresh after adding new statement files.

## API Endpoints

The app exposes several REST API endpoints:

- `GET /` - Main dashboard page
- `GET /api/summary` - Overall statistics and summaries
- `GET /api/transactions` - Filtered transaction list
- `GET /api/categories` - List of all categories
- `GET /api/months` - List of all months
- `GET /api/category/<name>` - Details for specific category
- `GET /api/reload` - Reload data from files

## Configuration

### Port and Host
Edit [app.py](app.py:335):
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Change `port=5000` to use a different port.

### Data Paths
The app looks for:
- Statements: `./statements/`
- Rules: `./rules.json`

To change these, edit the paths in `load_data()` function in [app.py](app.py).

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
source venv/bin/activate
pip install flask
```

### "Address already in use"
Port 5000 is taken. Either:
- Stop the other service using port 5000
- Change port in app.py

### "No transactions found"
- Check that `statements/` folder contains CSV files
- Verify file format matches expected structure
- Check console for error messages

### Changes Not Appearing
- Click **🔄 Reload Data** button
- Or restart the server (Ctrl+C, then `python3 app.py`)

### Browser Shows White Page
- Check browser console (F12) for JavaScript errors
- Ensure files in `static/` folder are accessible
- Check server console for error messages

## Features in Detail

### Summary Cards
Shows at-a-glance statistics:
- **Green** = Income/Positive
- **Red** = Expense/Negative
- Hover for subtle animation

### Category Cards
- Click to filter transactions by that category
- Color-coded amounts (green=income, red=expense)
- Shows transaction count

### Monthly Chart
- Simple bar chart of net per month
- Green bars = positive net
- Red bars = negative net
- Hover to see values

### Transaction Table
- Date, Description, Category, Amount, Balance
- Color-coded amounts
- Responsive design (scrolls on mobile)
- Pagination for large datasets

## Customization

### Colors
Edit [static/css/style.css](static/css/style.css):
- Income color: `.income { color: #10b981; }`
- Expense color: `.expense { color: #ef4444; }`
- Primary color: `#667eea` (used throughout)

### Page Size
Edit [static/js/app.js](static/js/app.js:4):
```javascript
const pageSize = 50;  // Change to show more/fewer per page
```

### Chart Height
Edit [static/css/style.css](static/css/style.css):
```css
.chart-container {
    height: 250px;  /* Adjust chart height */
}
```

## Advanced Usage

### Access from Another Device
If running on port 5000 with host `0.0.0.0`, access from other devices on same network:

```
http://YOUR_COMPUTER_IP:5000
```

Find your IP:
```bash
ip addr show  # Linux
ifconfig      # Mac
ipconfig      # Windows
```

### Run in Background
```bash
# Using nohup
nohup python3 app.py > app.log 2>&1 &

# Stop it later
pkill -f app.py
```

### Production Deployment
For production use, use a proper WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla JavaScript (no frameworks)
- **Data**: pandas for processing
- **Styling**: Custom CSS with gradients and animations

## File Structure

```
Statement/
├── app.py                    ← Flask server
├── templates/
│   └── index.html            ← Main page template
├── static/
│   ├── css/
│   │   └── style.css         ← Styles
│   └── js/
│       └── app.js            ← Frontend logic
├── parser.py                 ← Data loading (used by app.py)
├── categorizer.py            ← Categorization (used by app.py)
└── rules.json                ← Category rules
```

## Comparison: CLI vs Web App

| Feature | CLI (main.py) | Web App (app.py) |
|---------|---------------|------------------|
| Interface | Command line | Browser |
| Output | CSV files | Interactive dashboard |
| Filtering | Manual (open CSV) | Real-time filters |
| Charts | None | Visual charts |
| Search | None | Live search |
| Use Case | Export/Analysis | Exploration |

## Tips

1. **Use both**: CLI for exports, Web for exploration
2. **Filter early**: Use category/month filters before searching
3. **Bookmark filters**: Browser back button works
4. **Mobile friendly**: Works on phones/tablets
5. **Print reports**: Use browser print to PDF

## Next Steps

1. Run the web app: `python3 app.py`
2. Explore the interface
3. Try different filters
4. Drill down into categories
5. Export data if needed (use main.py)

---

**Need help?** Check the console for error messages or review [README.md](README.md) for general usage.
