# Installation Instructions

## Ubuntu/Debian Users (Quick Method)

### Option 1: Automated Setup Script

```bash
# Install system dependency
sudo apt install python3-venv

# Run setup script
./setup.sh
```

### Option 2: Manual Setup

```bash
# 1. Install system dependency
sudo apt install python3-venv

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install pandas
pip install pandas
```

## Every Time You Use the Tool

```bash
# 1. Activate virtual environment (REQUIRED)
source venv/bin/activate

# 2. Run analyzer
python3 main.py

# 3. When done, deactivate (optional)
deactivate
```

## Quick Test

```bash
# Activate venv
source venv/bin/activate

# Run with sample data
python3 main.py

# Check output
ls output/
```

## Troubleshooting

### "No module named 'pandas'"
You forgot to activate the virtual environment:
```bash
source venv/bin/activate
```

### "python3-venv not found"
On older Ubuntu versions:
```bash
sudo apt install python3.12-venv
```

### "Permission denied: ./setup.sh"
Make it executable:
```bash
chmod +x setup.sh
```

### Virtual environment exists but broken
Delete and recreate:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install pandas
```

## Verify Installation

```bash
source venv/bin/activate
python3 -c "import pandas; print('Pandas version:', pandas.__version__)"
```

Should output: `Pandas version: X.X.X`

## Next Steps

See [QUICK_START.md](QUICK_START.md) for usage instructions.
