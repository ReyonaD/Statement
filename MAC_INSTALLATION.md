# Bank Statement Analyzer - Mac Installation Guide

**For Non-Technical Users**

This guide will help you install and run the Bank Statement Analyzer on your Mac.

---

## Quick Start (3 Steps)

### Step 1: Install Python 3

1. Open Safari and go to: **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python 3.x.x"** button
3. Open the downloaded file and follow the installer
4. Click "Continue" → "Agree" → "Install"
5. Enter your Mac password when prompted
6. Click "Close" when done

**How to check if Python is already installed:**
- Open **Terminal** (search for "Terminal" in Spotlight)
- Type: `python3 --version`
- If you see "Python 3.x.x", you're good to go!

---

### Step 2: Get the Application Files

Your friend should give you a folder called **"Statement"**.

Copy this entire folder to your **Desktop** or **Documents** folder.

---

### Step 3: Run the Application

#### Method A: Double-Click (EASIEST!) ⭐

1. Open the **"Statement"** folder
2. Find the file called **"Bank Statement Analyzer.command"**
3. **Double-click** on it!
4. If you see a security warning:
   - Click **"Open"** when prompted
   - OR: Right-click → **"Open"** → Click **"Open"** again
5. The app will start automatically and open in your browser!

**That's it!** From now on, just double-click this file to start the app.

#### Method B: Alternative Launcher

1. Open the **"Statement"** folder
2. Find the file called **"mac-launcher.sh"**
3. **Right-click** on it and select **"Open With" → "Terminal"**
4. If you see a security warning, click **"Open"**
5. The app will start automatically!

#### Method C: Terminal (For Advanced Users)

1. Open **Terminal** (search for "Terminal" in Spotlight)
2. Type: `cd Desktop/Statement` (or wherever you put the folder)
3. Press Enter
4. Type: `bash mac-launcher.sh`
5. Press Enter

---

## What Will Happen

When you run the launcher, you'll see:

```
╔════════════════════════════════════════════════╗
║    Bank Statement Analyzer                    ║
║    Starting Application...                     ║
╔════════════════════════════════════════════════╗

✓ Python 3 found
✓ Virtual environment created (first time only)
✓ Dependencies installed (first time only)
✓ Setup complete!

🚀 Starting Bank Statement Analyzer...

The application will open in your browser at:
http://localhost:5000

⚠️  DO NOT CLOSE THIS WINDOW!
Keep this window open while using the app.

To stop the application: Press Ctrl+C
```

Your browser will automatically open and show the application!

---

## Using the Application

### Upload Your Bank Statement

1. Click the **"Files"** tab
2. Drag and drop your CSV file, OR
3. Click **"Choose File"** and select your statement

### View Your Data

- **Overview Tab**: See total income, expenses, and balance
- **Categories Tab**: See spending by category (Shopify, Zelle, etc.)
- **Monthly Tab**: See monthly trends
- **Transactions Tab**: See all transactions with filters
- **Files Tab**: Manage uploaded files

### Upload Multiple Accounts

You can upload statements from different bank accounts:
- Chase checking
- Savings account
- Business account

Use the **"View by Bank Account"** dropdown to switch between accounts!

---

## Stopping the Application

When you're done:

1. Go back to the Terminal window
2. Press **Ctrl + C** on your keyboard
3. OR just close the Terminal window

The browser tab will show an error - that's normal! Just close it.

---

## Troubleshooting

### Problem: "Python 3 is not installed"

**Solution:**
- Follow Step 1 above to install Python
- Download from: https://www.python.org/downloads/

---

### Problem: "Permission denied" when running mac-launcher.sh

**Solution:**
1. Open Terminal
2. Type: `cd Desktop/Statement` (or wherever your folder is)
3. Type: `chmod +x mac-launcher.sh`
4. Press Enter
5. Try running the launcher again

---

### Problem: Browser doesn't open automatically

**Solution:**
- Manually open Safari (or Chrome/Firefox)
- Go to: **http://localhost:5000**

---

### Problem: "Address already in use"

**Solution:**
The app might already be running!
1. Check if you have another Terminal window open
2. Close it and try again
3. OR restart your Mac

---

### Problem: Can't find the Statement folder

**Solution:**
- Make sure your friend gave you the complete folder
- It should contain these files:
  - mac-launcher.sh
  - app.py
  - requirements.txt
  - templates/ folder
  - static/ folder

---

### Problem: Upload fails or file not recognized

**Solution:**
- Make sure your file is in CSV format (.csv)
- Check that it has these columns: Date, Description, Amount, Balance
- Try opening the CSV in Excel/Numbers first to verify format

---

## File Locations

### Where are my uploaded files stored?

Inside the **Statement** folder, in the **"statements"** subfolder.

### Where are exported reports?

Inside the **Statement** folder, in the **"output"** subfolder.

---

## Security & Privacy

**Your data stays on your computer!**

- No internet connection required (after initial setup)
- No data is sent anywhere
- All processing happens locally on your Mac
- Your bank statements are stored only in the "statements" folder

---

## Updating the Application

If your friend gives you an updated version:

1. **Close the current app** (Ctrl+C in Terminal)
2. **Backup your data**:
   - Copy the "statements" folder somewhere safe
   - Copy the "output" folder somewhere safe
3. **Replace the old folder** with the new one
4. **Copy back your data**:
   - Put your "statements" folder back
   - Put your "output" folder back
5. **Run the launcher again**

---

## Uninstalling

To completely remove the application:

1. Close the app (Ctrl+C in Terminal)
2. Delete the **"Statement"** folder
3. Done!

Optional: Remove Python 3 (only if you don't need it for anything else)
- Open **Applications** folder
- Find **Python 3.x** folder
- Drag to Trash

---

## Getting Help

If you encounter issues:

1. **Check the Terminal window** for error messages
2. **Try restarting** the application
3. **Restart your Mac** if problems persist
4. **Ask your friend** who set this up for you

---

## Tips

### Tip 1: Create a Desktop Shortcut

Make it even easier to launch:
1. Find **"Bank Statement Analyzer.command"** in the Statement folder
2. Hold **Option + Command** and drag it to your Desktop (creates an alias)
3. Now you can double-click from your Desktop anytime!

Or manually:
1. Right-click **"Bank Statement Analyzer.command"**
2. Select **"Make Alias"**
3. Drag the alias to your Desktop

### Tip 2: Organize Your Statements

Keep your bank statement files organized:
```
Documents/
  Bank Statements/
    2025/
      01-January/
        chase-checking-2025-01.csv
        savings-2025-01.csv
      02-February/
        chase-checking-2025-02.csv
```

### Tip 3: Regular Backups

Backup the entire **Statement** folder regularly:
- To external drive
- To iCloud Drive
- To Time Machine

---

## System Requirements

- **Mac OS**: 10.13 (High Sierra) or newer
- **Python**: 3.8 or newer
- **Disk Space**: ~100 MB for application + your statement files
- **RAM**: 2 GB minimum
- **Browser**: Safari, Chrome, Firefox, or Edge

---

## Advanced: Running in Background

If you want to keep using Terminal while the app runs:

Instead of `bash mac-launcher.sh`, use:
```bash
bash mac-launcher.sh &
```

The `&` at the end runs it in the background.

To stop it later:
```bash
killall python3
```

---

## Questions?

**Q: Can I use this on Windows?**
A: Not with this launcher. Ask your friend for a Windows version.

**Q: Does this work offline?**
A: Yes! After the first setup (which downloads dependencies), everything works offline.

**Q: Can multiple people use this?**
A: One person at a time on each computer. Each user should have their own copy.

**Q: Will this slow down my Mac?**
A: No, it uses minimal resources and only runs when you start it.

**Q: Is my financial data safe?**
A: Yes! Everything stays on your Mac. No data is uploaded anywhere.

---

## Success!

You should now see the Bank Statement Analyzer running in your browser!

Upload your first statement and start analyzing! 🎉

---

**Created for non-technical Mac users**
**Version 1.0 - 2025**
