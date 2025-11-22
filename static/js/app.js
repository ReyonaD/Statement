// Bank Statement Analyzer - Frontend JavaScript

let summaryData = null;
let currentPage = 0;
const pageSize = 50;

// Initialize app on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSourceFiles();
    loadSummary();
    loadCategories();
    loadMonths();
    loadTransactions();
});

// Load source files for filter dropdown
async function loadSourceFiles() {
    try {
        const response = await fetch('/api/source-files');
        const data = await response.json();

        // Populate main filter dropdown
        const mainSelect = document.getElementById('sourceFileFilter');
        const transSelect = document.getElementById('filterSourceFile');

        if (mainSelect) {
            // Clear existing options except "All"
            mainSelect.innerHTML = '<option value="all">All Accounts (Combined)</option>';

            data.source_files.forEach(sf => {
                const option = document.createElement('option');
                option.value = sf.source_file;
                option.textContent = `${sf.source_file} (${sf.count} transactions)`;
                mainSelect.appendChild(option);
            });
        }

        if (transSelect) {
            transSelect.innerHTML = '<option value="all">All Accounts</option>';

            data.source_files.forEach(sf => {
                const option = document.createElement('option');
                option.value = sf.source_file;
                option.textContent = sf.source_file;
                transSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading source files:', error);
    }
}

// Filter by source file from main dropdown
function filterBySourceFile() {
    loadSummary();
    loadTransactions();
}

// Load summary data
async function loadSummary() {
    try {
        const sourceFile = document.getElementById('sourceFileFilter')?.value || 'all';
        const params = new URLSearchParams();
        if (sourceFile && sourceFile !== 'all') {
            params.append('source_file', sourceFile);
        }

        const response = await fetch(`/api/summary?${params}`);
        const data = await response.json();
        summaryData = data;

        // Update summary cards
        document.getElementById('startingBalance').textContent = formatCurrency(data.overall.starting_balance);
        document.getElementById('startingDate').textContent = `as of ${data.overall.start_date}`;
        document.getElementById('endingBalance').textContent = formatCurrency(data.overall.ending_balance);
        document.getElementById('endingDate').textContent = `as of ${data.overall.end_date}`;
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
    const sourceFile = document.getElementById('filterSourceFile')?.value ||
                      document.getElementById('sourceFileFilter')?.value || 'all';
    const category = document.getElementById('filterCategory')?.value || 'all';
    const month = document.getElementById('filterMonth')?.value || 'all';
    const type = document.getElementById('filterType')?.value || 'all';
    const search = document.getElementById('filterSearch')?.value || '';

    const params = new URLSearchParams({
        source_file: sourceFile,
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

            // Use amount sign to determine color
            // Negative amounts = expense (red), Positive amounts = income (green)
            const isExpense = txn.amount < 0;

            // Add tooltip to show source file
            row.title = `Source: ${txn.source_file}`;
            row.style.cursor = 'help';

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

// File upload functionality
function setupDragAndDrop() {
    const uploadArea = document.getElementById('uploadArea');

    if (!uploadArea) return;

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        uploadFiles(files);
    });
}

function handleFileSelect(event) {
    const files = event.target.files;
    uploadFiles(files);
}

async function uploadFiles(files) {
    const results = document.getElementById('uploadResults');
    const progress = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');
    const uploadStatus = document.getElementById('uploadStatus');

    results.innerHTML = '';
    progress.style.display = 'block';

    const totalFiles = files.length;
    let uploadedFiles = 0;
    let successCount = 0;
    let errorCount = 0;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];

        // Check file type
        if (!file.name.endsWith('.csv') && !file.name.endsWith('.txt')) {
            addUploadResult(file.name, false, 'Invalid file type. Only CSV and TXT files allowed.');
            errorCount++;
            uploadedFiles++;
            updateProgress(uploadedFiles, totalFiles, progressFill, uploadStatus);
            continue;
        }

        // Upload file
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                addUploadResult(file.name, true, data.message);
                successCount++;
            } else {
                addUploadResult(file.name, false, data.error);
                errorCount++;
            }
        } catch (error) {
            addUploadResult(file.name, false, `Upload failed: ${error.message}`);
            errorCount++;
        }

        uploadedFiles++;
        updateProgress(uploadedFiles, totalFiles, progressFill, uploadStatus);
    }

    // Hide progress after delay
    setTimeout(() => {
        progress.style.display = 'none';
        progressFill.style.width = '0%';
    }, 2000);

    // Reload file list and data
    if (successCount > 0) {
        loadFiles();
        setTimeout(() => {
            loadSourceFiles();
            loadSummary();
            loadTransactions();
        }, 500);
    }

    // Reset file input
    document.getElementById('fileInput').value = '';
}

function updateProgress(uploaded, total, progressFill, uploadStatus) {
    const percent = (uploaded / total) * 100;
    progressFill.style.width = `${percent}%`;
    uploadStatus.textContent = `Uploading... ${uploaded}/${total} files`;

    if (uploaded === total) {
        uploadStatus.textContent = 'Upload complete!';
    }
}

function addUploadResult(filename, success, message) {
    const results = document.getElementById('uploadResults');

    const resultDiv = document.createElement('div');
    resultDiv.className = `upload-result ${success ? 'success' : 'error'}`;

    resultDiv.innerHTML = `
        <span class="result-icon">${success ? '✓' : '✗'}</span>
        <span class="result-filename">${escapeHtml(filename)}</span>
        <span class="result-message">${escapeHtml(message)}</span>
    `;

    results.appendChild(resultDiv);
}

// Load uploaded files
async function loadFiles() {
    try {
        const response = await fetch('/api/files');
        const data = await response.json();

        const fileList = document.getElementById('fileList');
        fileList.innerHTML = '';

        if (data.files.length === 0) {
            fileList.innerHTML = '<p class="no-files">No files uploaded yet. Upload your first statement file above!</p>';
            return;
        }

        data.files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';

            const sizeKB = (file.size / 1024).toFixed(1);

            fileItem.innerHTML = `
                <div class="file-info">
                    <div class="file-name">📄 ${escapeHtml(file.name)}</div>
                    <div class="file-meta">
                        <span>${sizeKB} KB</span>
                        <span>Modified: ${file.modified}</span>
                    </div>
                </div>
                <button class="btn-delete" onclick="deleteFile('${escapeHtml(file.name)}')">
                    🗑️ Delete
                </button>
            `;

            fileList.appendChild(fileItem);
        });

    } catch (error) {
        console.error('Error loading files:', error);
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = '<p class="error">Error loading files</p>';
    }
}

// Delete file
async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/files/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            loadFiles();
            loadSourceFiles();
            loadSummary();
            loadTransactions();
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error deleting file:', error);
        alert('Error deleting file');
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

// Initialize drag and drop when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupDragAndDrop();

    // Load files list when Files tab is opened
    const filesTab = document.querySelector('.tab:nth-child(5)');
    if (filesTab) {
        filesTab.addEventListener('click', () => {
            loadFiles();
        });
    }
});
