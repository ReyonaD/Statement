# File Upload Guide

## Upload Your Bank Statements via Web Interface

No need to manually copy files! Upload your bank statements directly through the browser.

## How to Upload Files

### Method 1: Drag & Drop (Recommended)

1. Launch the web app: `./run.sh`
2. Open http://localhost:5000
3. Click the **📂 Files** tab
4. **Drag your CSV/TXT files** into the upload area
5. Watch the progress bar as files upload
6. Data automatically refreshes!

### Method 2: Browse Files

1. Click the **📂 Files** tab
2. Click **"Browse Files"** button
3. Select one or multiple CSV/TXT files
4. Files upload automatically
5. Dashboard updates with new data

## Supported Files

✅ **CSV files** (.csv)
✅ **TXT files** (.txt)
📦 **Max size**: 16MB per file
🔢 **Multiple files**: Upload many at once

## File Format

Your files should have this format:
```
Date,Description,Amount,Running Balance
01/08/2025,SHOPIFY PAYMENTS,"2,408.66","52,408.66"
```

## Features

### Upload Progress
- Real-time progress bar
- Shows "X/Y files" uploaded
- Success/error messages for each file

### File Management
- **View all uploaded files**
  - File name
  - File size
  - Last modified date

- **Delete files**
  - Click 🗑️ Delete button
  - Confirm deletion
  - Data automatically refreshes

### Auto-Refresh
After successful upload:
- Summary cards update automatically
- Categories recalculate
- Transactions reload
- Charts refresh

## Example Workflow

```bash
# 1. Start the app
./run.sh

# 2. Open browser
# Go to: http://localhost:5000

# 3. Click "Files" tab

# 4. Drag your statement files into the upload area
# Example: 07ISAD stmt.csv, 08ISAD stmt.csv, etc.

# 5. Wait for "Upload complete!"

# 6. Click "Overview" tab to see updated totals
```

## Upload Multiple Months

Upload all your statement files at once:

1. Select multiple files (Ctrl+Click or Cmd+Click)
2. Or drag multiple files together
3. All files upload sequentially
4. Progress shows: "Uploading... 3/5 files"
5. See results for each file

## Manage Uploaded Files

### View Files
The **Uploaded Files** section shows:
- 📄 File name
- File size (in KB)
- Last modified timestamp
- Delete button

### Delete Files
To remove a file:
1. Click 🗑️ Delete next to the file
2. Confirm the deletion
3. File removed from `statements/` folder
4. Data reloads without that file

## Troubleshooting

### "Invalid file type"
- Only CSV and TXT files allowed
- Check file extension

### "File too large"
- Maximum 16MB per file
- Split large files if needed

### "Upload failed"
- Check internet connection
- Ensure server is running
- Check browser console (F12) for errors

### Files not appearing
- Click 🔄 Reload Data button
- Or refresh the browser page

### Upload hangs
- Check file size (max 16MB)
- Check file format
- Restart the server

## Security Notes

- Files saved to: `./statements/` folder
- File names are sanitized for security
- Only CSV/TXT extensions allowed
- No executable files accepted
- 16MB size limit prevents abuse

## Advanced Tips

### 1. Upload from Mobile
- Works on phones/tablets
- Tap "Browse Files" to select from device
- Drag-and-drop may not work on mobile

### 2. Batch Upload
- Select 10+ files at once
- Upload all monthly statements together
- Watch progress bar

### 3. Replace Files
- Upload file with same name
- Overwrites existing file
- Or delete old file first

### 4. Organize Files
- Name files clearly: `2025-07.csv`, `2025-08.csv`
- Use consistent naming
- Easier to manage later

## Comparison: Upload vs Manual Copy

| Feature | Web Upload | Manual Copy |
|---------|------------|-------------|
| Convenience | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Speed | Fast | Slow |
| Multiple files | Yes | Yes |
| Progress feedback | Yes | No |
| Auto-refresh | Yes | Manual |
| Delete files | Via UI | Terminal |
| Mobile friendly | Yes | No |

## What Happens After Upload?

1. **File saved** to `statements/` folder
2. **Parser runs** automatically
3. **Categorization** applies rules.json
4. **Dashboard updates** with new data
5. **You see** updated totals, categories, transactions

## API Endpoints (for developers)

```
POST /api/upload
  - Upload a file
  - Returns: {success, filename, message}

GET /api/files
  - List all uploaded files
  - Returns: {files: [{name, size, modified}]}

DELETE /api/files/<filename>
  - Delete a specific file
  - Returns: {success, message}
```

## Next Steps

1. **Upload your files** via the Files tab
2. **Explore data** in Overview/Categories/Transactions
3. **Add categories** in rules.json as needed
4. **Upload more** as you get new statements

---

**Ready to upload?** Run `./run.sh` and click the **📂 Files** tab!
