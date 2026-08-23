# TeraBox Integration Skill

## Overview

This skill provides cloud storage operations via browser automation and API integration with TeraBox.

## Features

- **Browser Authentication**: Extract cookies from logged-in Playwright session
- **File Upload**: Upload files via hidden input elements
- **Folder Upload**: Upload entire directory structures
- **API Integration**: Check quota, list files, verify uploads
- **Compression**: Automatic zip compression for batch uploads

## Installation

1. Install Python dependencies:
   ```bash
   pip install playwright requests
   ```

2. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

## Usage

### PowerShell Commands

```powershell
# Set environment
$env:PYTHONIOENCODING='utf-8'
$py = "C:\Users\Abdox\AppData\Local\Python\bin\python3.14-64.exe"
$terabox = "C:\opencodes\guard skills\skills\tools\terabox-integration\terabox.py"

# Check storage quota
& $py $terabox quota

# List files in root directory
& $py $terabox list

# Upload a file
& $py $terabox upload "C:\path\to\file.zip"

# Upload a folder (compresses first)
& $py $terabox upload-folder "C:\path\to\folder"

# Verify upload
& $py $terabox verify "filename.zip"
```

### Python API

```python
from terabox import TeraBoxIntegration

# Initialize
tb = TeraBoxIntegration()

# Extract cookies from browser
cookies = tb.extract_cookies_from_browser()

# Check quota
quota = tb.check_quota()
print(f"Storage: {quota['used']/1024**3:.1f} GB / {quota['total']/1024**3:.0f} GB")

# List files
files = tb.list_files()
for f in files:
    print(f.get('server_filename'))

# Upload file
tb.upload_file("document.pdf")

# Upload folder
tb.upload_folder("C:\\projects\\my-project")
```

## API Endpoints

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/api/quota` | Check storage space | GET |
| `/api/list` | List files/directories | GET |
| `/api/precreate` | Initialize upload | POST |
| `/api/create` | Finalize upload | POST |

## Authentication

The tool uses cookie-based authentication extracted from a Playwright browser session. Required cookies:

- `ndus`: User session identifier
- `ndut_fmt`: Session format
- `browserid`: Browser identifier
- `csrfToken`: CSRF protection token
- `lang`: Language preference

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `precreate fail` | Session expired | Re-authenticate via browser |
| `login session has expired` | Cookie mismatch | Update cookies from browser |
| `quota exceeded` | Storage full | Delete files or upgrade plan |
| `file not found` | Invalid path | Check local file path |

## Security Considerations

- Cookies are stored in memory only (not persisted)
- Browser session must be active for authentication
- API calls use `credentials: include` for cookie-based auth
- No secrets or tokens hardcoded in scripts

## File Structure

```
terabox-integration/
├── SKILL.md          # Skill documentation
├── terabox.py        # Main implementation
└── README.md         # This file
```

## Version History

- **v1.0.0**: Initial release with basic upload functionality
- **v1.1.0**: Added folder upload and compression
- **v1.2.0**: Added API quota checking and file listing

## License

Internal use only - Guard Skills Project