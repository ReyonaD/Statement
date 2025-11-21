// Bank Statement Analyzer - Frontend JavaScript

let summaryData = null;
let currentPage = 0;
const pageSize = 50;

// Initialize app on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSummary();
    loadCategories();
    loadMonths();
    loadTransactions();
});

// Load summary data
async function loadSummary() {
    try {
        const response = await fetch('/api/summary');
        const data = await response.json();
        summaryData = data;

        // Update summary cards
        document.getElementById('totalIncome').textContent = formatCurrency(data.overall.total_income);
        document.getElementById('totalExpense').textContent = formatCurrency(data.overall.total_expense);
        document.getElementById('net').textContent = formatCurrency(data.overall.net);
        document.getElementById('totalTransactions').textContent = data.overall.total_transactions.toLocaleString();

        // Set net color
        const netElement = document.getElementById('net');
        if (data.overall.net >= 0) {
            netElement.classList.add('income');
            netElement.classList.remove('expense');
        } else {
            netElement.classList.add('expense');
            netElement.classList.remove('income');
        }

        // Populate category grid
        populateCategoryGrid(data.categories);

        // Populate monthly grid
        populateMonthlyGrid(data.monthly);

        // Populate category list (detailed view)
        populateCategoryList(data.categories);

    } catch (error) {
        console.error('Error loading summary:', error);
        alert('Error loading data. Please check console.');
    }
}

// Populate category grid in overview
function populateCategoryGrid(categories) {
    const grid = document.getElementById('categoryGrid');
    grid.innerHTML = '';

    categories.forEach(cat => {
        const card = document.createElement('div');
        card.className = 'category-card';
        card.onclick = () => {
            showTab('transactions');
            document.getElementById('filterCategory').value = cat.category;
            filterTransactions();
        };

        const isExpense = cat.total < 0;

        card.innerHTML = `
            <div class="category-name">${cat.category}</div>
            <div class="category-amount ${isExpense ? 'expense' : 'income'}">
                ${formatCurrency(cat.total)}
            </div>
            <div class="category-count">${cat.count} transactions</div>
        `;

        grid.appendChild(card);
    });
}

// Populate category list (detailed view)
function populateCategoryList(categories) {
    const list = document.getElementById('categoryList');
    list.innerHTML = '';

    categories.forEach(cat => {
        const item = document.createElement('div');
        item.className = 'category-detail-item';

        const isExpense = cat.total < 0;
        const avgAmount = cat.total / cat.count;

        item.innerHTML = `
            <div class="category-header">
                <h3>${cat.category}</h3>
                <div class="category-amount ${isExpense ? 'expense' : 'income'}">
                    ${formatCurrency(cat.total)}
                </div>
            </div>
            <div class="category-stats">
                <span>${cat.count} transactions</span>
                <span>Average: ${formatCurrency(avgAmount)}</span>
            </div>
            <button class="btn-view" onclick="viewCategoryTransactions('${cat.category}')">
                View Transactions
            </button>
        `;

        list.appendChild(item);
    });
}

// Populate monthly grid
function populateMonthlyGrid(monthly) {
    const grid = document.getElementById('monthlyGrid');
    grid.innerHTML = '';

    // Also create simple chart in overview
    const chart = document.getElementById('monthlyChart');
    chart.innerHTML = '';

    monthly.forEach(month => {
        // Monthly detail card
        const card = document.createElement('div');
        card.className = 'monthly-card';

        card.innerHTML = `
            <div class="month-name">${month.month}</div>
            <div class="month-stats">
                <div class="stat-row">
                    <span>Income:</span>
                    <span class="income">${formatCurrency(month.income)}</span>
                </div>
                <div class="stat-row">
                    <span>Expense:</span>
                    <span class="expense">${formatCurrency(month.expense)}</span>
                </div>
                <div class="stat-row">
                    <span>Net:</span>
                    <span class="${month.net >= 0 ? 'income' : 'expense'}">${formatCurrency(month.net)}</span>
                </div>
                <div class="stat-row">
                    <span>Transactions:</span>
                    <span>${month.count}</span>
                </div>
            </div>
            <button class="btn-view" onclick="viewMonthTransactions('${month.month}')">
                View Details
            </button>
        `;

        grid.appendChild(card);

        // Simple bar chart
        const bar = document.createElement('div');
        bar.className = 'chart-bar';

        const maxAmount = Math.max(...monthly.map(m => Math.abs(m.net)));
        const barHeight = Math.abs(month.net) / maxAmount * 200;
        const barColor = month.net >= 0 ? '#10b981' : '#ef4444';

        bar.innerHTML = `
            <div class="bar" style="height: ${barHeight}px; background-color: ${barColor}"></div>
            <div class="bar-label">${month.month.substring(5)}</div>
            <div class="bar-value">${formatCurrency(month.net)}</div>
        `;

        chart.appendChild(bar);
    });
}

// Load categories for filter dropdown
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();

        const select = document.getElementById('filterCategory');
        data.categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load months for filter dropdown
async function loadMonths() {
    try {
        const response = await fetch('/api/months');
        const data = await response.json();

        const select = document.getElementById('filterMonth');
        data.months.forEach(month => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading months:', error);
    }
}

// Load and display transactions with filters
async function loadTransactions() {
    const category = document.getElementById('filterCategory')?.value || 'all';
    const month = document.getElementById('filterMonth')?.value || 'all';
    const type = document.getElementById('filterType')?.value || 'all';
    const search = document.getElementById('filterSearch')?.value || '';

    const params = new URLSearchParams({
        category,
        month,
        type,
        search,
        limit: pageSize,
        offset: currentPage * pageSize
    });

    try {
        const response = await fetch(`/api/transactions?${params}`);
        const data = await response.json();

        const tbody = document.getElementById('transactionTableBody');
        tbody.innerHTML = '';

        data.transactions.forEach(txn => {
            const row = document.createElement('tr');
            const isExpense = txn.amount < 0;

            row.innerHTML = `
                <td>${txn.date}</td>
                <td class="description">${escapeHtml(txn.description)}</td>
                <td><span class="category-badge">${txn.category}</span></td>
                <td class="${isExpense ? 'expense' : 'income'}">${formatCurrency(txn.amount)}</td>
                <td>${txn.balance ? formatCurrency(txn.balance) : '-'}</td>
            `;

            tbody.appendChild(row);
        });

        // Update count
        document.getElementById('transactionCount').textContent =
            `Showing ${data.transactions.length} of ${data.total_count} transactions`;

        // Update pagination
        updatePagination(data.total_count);

    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

// Filter transactions
function filterTransactions() {
    currentPage = 0;
    loadTransactions();
}

// Update pagination controls
function updatePagination(totalCount) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const totalPages = Math.ceil(totalCount / pageSize);

    if (totalPages <= 1) return;

    // Previous button
    if (currentPage > 0) {
        const prev = document.createElement('button');
        prev.textContent = '← Previous';
        prev.className = 'btn-page';
        prev.onclick = () => {
            currentPage--;
            loadTransactions();
        };
        pagination.appendChild(prev);
    }

    // Page info
    const info = document.createElement('span');
    info.textContent = `Page ${currentPage + 1} of ${totalPages}`;
    info.className = 'page-info';
    pagination.appendChild(info);

    // Next button
    if (currentPage < totalPages - 1) {
        const next = document.createElement('button');
        next.textContent = 'Next →';
        next.className = 'btn-page';
        next.onclick = () => {
            currentPage++;
            loadTransactions();
        };
        pagination.appendChild(next);
    }
}

// View transactions for specific category
function viewCategoryTransactions(category) {
    showTab('transactions');
    document.getElementById('filterCategory').value = category;
    filterTransactions();
}

// View transactions for specific month
function viewMonthTransactions(month) {
    showTab('transactions');
    document.getElementById('filterMonth').value = month;
    filterTransactions();
}

// Show/hide tabs
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active from all tab buttons
    document.querySelectorAll('.tab').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName + 'Tab').classList.add('active');

    // Activate button
    event.target.classList.add('active');
}

// Reload data
async function reloadData() {
    try {
        const response = await fetch('/api/reload');
        const data = await response.json();

        if (data.success) {
            alert('Data reloaded successfully!');
            location.reload();
        } else {
            alert('Error reloading data');
        }
    } catch (error) {
        console.error('Error reloading data:', error);
        alert('Error reloading data');
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
