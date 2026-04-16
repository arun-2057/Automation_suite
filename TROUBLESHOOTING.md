# Automation Suite - Troubleshooting Guide

## Common Issues and Solutions

### 1. Installation Issues

#### Issue: `python-magic` import error
**Error:** `ImportError: failed to find libmagic. Check your installation`

**Solution:**
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get install libmagic1
  pip install python-magic
  ```
- **macOS:**
  ```bash
  brew install libmagic
  pip install python-magic
  ```
- **Windows:**
  - python-magic requires additional setup on Windows
  - Consider using the alternative file detection methods or skip this optional dependency
  - The core functionality works without python-magic

#### Issue: Missing dependencies
**Error:** `ModuleNotFoundError: No module named 'PyPDF2'` (or other packages)

**Solution:**
```bash
pip install -r requirements.txt
```

If that fails, install individually:
```bash
pip install PyPDF2 pandas requests beautifulsoup4
```

### 2. Runtime Issues

#### Issue: File Organizer not moving files
**Possible Causes:**
- Config file not found
- Insufficient permissions
- Files already organized

**Solution:**
1. Verify config.json exists in the file_organizer directory
2. Check file permissions
3. Ensure files match the extensions in config.json

#### Issue: Web Scraper returns no headlines
**Possible Causes:**
- Website structure changed
- Network connectivity issues
- Rate limiting

**Solution:**
1. Check your internet connection
2. Try a different URL
3. Wait a few minutes and retry
4. Check if the website blocks automated access

#### Issue: Document Extractor fails on PDF
**Possible Causes:**
- Corrupted PDF file
- Encrypted PDF
- Unsupported PDF format

**Solution:**
1. Verify the PDF opens in a PDF reader
2. Remove password protection if encrypted
3. Try converting to a different PDF version

### 3. Logging Issues

#### Issue: No logs being created
**Solution:**
1. Check if the `logs` directory exists
2. Verify write permissions in the project directory
3. Check log file path in utils/logger.py

### 4. Performance Issues

#### Issue: Slow file organization
**Solution:**
- Organize files in smaller batches
- Exclude large files or specific directories
- Run during off-peak hours

#### Issue: Web scraping timeout
**Solution:**
- Increase timeout in scraper.py
- Check network speed
- Reduce number of concurrent requests

### 5. Platform-Specific Issues

#### Windows
- Use forward slashes (/) or double backslashes (\\) in file paths
- Run as Administrator if permission errors occur
- Use PowerShell or Command Prompt (not Git Bash for some operations)

#### macOS/Linux
- Ensure execute permissions: `chmod +x main.py`
- Use `python3` instead of `python` if multiple versions installed
- Check SELinux/AppArmor policies if files can't be accessed

### 6. Getting Help

If you encounter issues not covered here:

1. **Check the logs:** `logs/automation_suite.log`
2. **Verify Python version:** `python --version` (should be 3.8+)
3. **Reinstall dependencies:** `pip install -r requirements.txt --force-reinstall`
4. **Update the project:** Pull latest changes from repository
5. **Open an issue:** Include error messages, Python version, and OS details

### Quick Diagnostic Commands

```bash
# Check Python version
python --version

# Verify dependencies
pip list | grep -E "PyPDF2|pandas|requests|beautifulsoup4"

# Test imports
python -c "import PyPDF2, pandas, requests, bs4; print('All good!')"

# Check file permissions
ls -la

# View recent logs
tail -n 50 logs/automation_suite.log
```

## Still Having Issues?

1. Make sure you're running from the project root directory
2. Verify all files are present and not corrupted
3. Try running with verbose logging enabled
4. Check GitHub Issues for similar problems
5. Contact the maintainers with detailed error information
