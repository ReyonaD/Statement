#!/usr/bin/env python3
"""
Bank Statement Analyzer - Web Application

Interactive visual dashboard for exploring bank transactions.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename

from parser import load_all_statements
from categorizer import apply_categories, load_rules

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './statements'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'csv', 'txt'}

# Global data store
data = {
    'transactions': None,
    'last_loaded': None,
    'rules': None
}


def load_data():
    """Load transaction data and rules."""
    global data

    try:
        # Load statements
        df = load_all_statements('./statements')

        # Check if empty
        if df.empty:
            print("No transaction data found. Upload some files to get started!")
            data['transactions'] = pd.DataFrame(columns=['date', 'description', 'amount', 'running_balance', 'source_file', 'category', 'month', 'year'])
            data['last_loaded'] = datetime.now()
            data['rules'] = load_rules('./rules.json')
            return True

        # Apply categorization
        df = apply_categories(df, './rules.json')

        # Add month column for grouping
        df['month'] = df['date'].dt.to_period('M').astype(str)

        # Add year-month for easier filtering
        df['year'] = df['date'].dt.year

        # Sort by date descending (most recent first)
        df = df.sort_values('date', ascending=False)

        data['transactions'] = df
        data['last_loaded'] = datetime.now()
        data['rules'] = load_rules('./rules.json')

        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        # Initialize empty dataframe on error
        data['transactions'] = pd.DataFrame(columns=['date', 'description', 'amount', 'running_balance', 'source_file', 'category', 'month', 'year'])
        data['last_loaded'] = datetime.now()
        try:
            data['rules'] = load_rules('./rules.json')
        except:
            data['rules'] = []
        return False


@app.route('/')
def index():
    """Main dashboard page."""
    if data['transactions'] is None:
        load_data()

    return render_template('index.html')


@app.route('/api/summary')
def api_summary():
    """Get overall summary statistics."""
    if data['transactions'] is None:
        load_data()

    df = data['transactions']

    # Filter by source file if specified
    source_file = request.args.get('source_file')
    if source_file and source_file != 'all':
        df = df[df['source_file'] == source_file]

    # Handle empty dataframe
    if df.empty:
        return jsonify({
            'overall': {
                'total_transactions': 0,
                'total_income': 0.0,
                'total_expense': 0.0,
                'net': 0.0,
                'date_range': 'No data'
            },
            'categories': [],
            'monthly': []
        })

    # Overall stats
    total_transactions = len(df)
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expense = df[df['amount'] < 0]['amount'].sum()
    net = total_income + total_expense

    # Date range
    date_min = df['date'].min().strftime('%Y-%m-%d')
    date_max = df['date'].max().strftime('%Y-%m-%d')

    # Category breakdown
    category_summary = df.groupby('category').agg({
        'amount': ['sum', 'count']
    }).reset_index()
    category_summary.columns = ['category', 'total', 'count']
    category_summary = category_summary.sort_values('total', key=abs, ascending=False)

    # Monthly breakdown
    monthly = df.groupby('month').agg({
        'amount': [
            lambda x: x[x > 0].sum(),  # income
            lambda x: x[x < 0].sum(),  # expense
            'sum',  # net
            'count'
        ]
    }).reset_index()
    monthly.columns = ['month', 'income', 'expense', 'net', 'count']
    monthly = monthly.sort_values('month')

    return jsonify({
        'overall': {
            'total_transactions': int(total_transactions),
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'net': float(net),
            'date_range': f"{date_min} to {date_max}"
        },
        'categories': category_summary.to_dict('records'),
        'monthly': monthly.to_dict('records')
    })


@app.route('/api/transactions')
def api_transactions():
    """Get filtered transaction list."""
    if data['transactions'] is None:
        load_data()

    df = data['transactions'].copy()

    # Get filter parameters
    source_file = request.args.get('source_file')
    category = request.args.get('category')
    month = request.args.get('month')
    search = request.args.get('search')
    transaction_type = request.args.get('type')  # 'income', 'expense', or 'all'

    # Apply filters
    if source_file and source_file != 'all':
        df = df[df['source_file'] == source_file]

    if category and category != 'all':
        df = df[df['category'] == category]

    if month and month != 'all':
        df = df[df['month'] == month]

    if search:
        df = df[df['description'].str.contains(search, case=False, na=False)]

    if transaction_type == 'income':
        df = df[df['amount'] > 0]
    elif transaction_type == 'expense':
        df = df[df['amount'] < 0]

    # Limit results
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))

    total_count = len(df)
    df = df.iloc[offset:offset+limit]

    # Convert to JSON-friendly format
    transactions = []
    for _, row in df.iterrows():
        transactions.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'description': row['description'],
            'amount': float(row['amount']),
            'balance': float(row['running_balance']) if pd.notna(row['running_balance']) else None,
            'category': row['category'],
            'source_file': row['source_file']
        })

    return jsonify({
        'transactions': transactions,
        'total_count': total_count,
        'offset': offset,
        'limit': limit
    })


@app.route('/api/categories')
def api_categories():
    """Get list of all categories."""
    if data['transactions'] is None:
        load_data()

    categories = sorted(data['transactions']['category'].unique().tolist())

    return jsonify({'categories': categories})


@app.route('/api/months')
def api_months():
    """Get list of all months."""
    if data['transactions'] is None:
        load_data()

    months = sorted(data['transactions']['month'].unique().tolist(), reverse=True)

    return jsonify({'months': months})


@app.route('/api/source-files')
def api_source_files():
    """Get list of all source files with transaction counts."""
    if data['transactions'] is None:
        load_data()

    df = data['transactions']

    if df.empty:
        return jsonify({'source_files': []})

    # Group by source file
    source_summary = df.groupby('source_file').agg({
        'amount': ['count', 'sum']
    }).reset_index()
    source_summary.columns = ['source_file', 'count', 'total']

    # Sort by file name
    source_summary = source_summary.sort_values('source_file')

    return jsonify({
        'source_files': source_summary.to_dict('records')
    })


@app.route('/api/category/<category_name>')
def api_category_detail(category_name):
    """Get detailed breakdown for a specific category."""
    if data['transactions'] is None:
        load_data()

    df = data['transactions']
    category_df = df[df['category'] == category_name]

    if category_df.empty:
        return jsonify({'error': 'Category not found'}), 404

    # Summary stats
    total = category_df['amount'].sum()
    count = len(category_df)
    avg = category_df['amount'].mean()

    # Monthly breakdown
    monthly = category_df.groupby('month')['amount'].agg(['sum', 'count']).reset_index()
    monthly.columns = ['month', 'total', 'count']
    monthly = monthly.sort_values('month')

    # Top descriptions
    top_desc = category_df.groupby('description')['amount'].agg(['sum', 'count']).reset_index()
    top_desc.columns = ['description', 'total', 'count']
    top_desc = top_desc.sort_values('total', key=abs, ascending=False).head(10)

    return jsonify({
        'category': category_name,
        'summary': {
            'total': float(total),
            'count': int(count),
            'average': float(avg)
        },
        'monthly': monthly.to_dict('records'),
        'top_descriptions': top_desc.to_dict('records')
    })


@app.route('/api/reload')
def api_reload():
    """Reload data from files."""
    success = load_data()
    return jsonify({'success': success})


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only CSV and TXT files allowed'}), 400

    try:
        # Secure the filename
        filename = secure_filename(file.filename)

        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Reload data
        load_data()

        return jsonify({
            'success': True,
            'filename': filename,
            'message': f'File {filename} uploaded successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/files')
def api_files():
    """Get list of uploaded files."""
    try:
        statements_path = Path(app.config['UPLOAD_FOLDER'])

        if not statements_path.exists():
            return jsonify({'files': []})

        files = []
        for file_path in statements_path.glob('*'):
            if file_path.is_file() and allowed_file(file_path.name):
                stat = file_path.stat()
                files.append({
                    'name': file_path.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })

        # Sort by modified date, most recent first
        files.sort(key=lambda x: x['modified'], reverse=True)

        return jsonify({'files': files})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/files/<filename>', methods=['DELETE'])
def api_delete_file(filename):
    """Delete an uploaded file."""
    try:
        # Secure the filename
        filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        # Delete file
        os.remove(filepath)

        # Reload data
        load_data()

        return jsonify({
            'success': True,
            'message': f'File {filename} deleted successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("="*60)
    print("Bank Statement Analyzer - Web Application")
    print("="*60)
    print("\nLoading data...")

    if load_data():
        print(f"✓ Loaded {len(data['transactions'])} transactions")
        print("\nStarting web server...")
        print("\n🌐 Open your browser to: http://localhost:5000")
        print("\nPress Ctrl+C to stop the server")
        print("="*60)
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("ERROR: Could not load data. Check that statements folder contains CSV files.")
