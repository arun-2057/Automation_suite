# File Organizer Tool

This tool automatically organizes files inside a folder based on file extensions.

## How It Works
- Reads extension mappings from config.json  
- Creates folders automatically  
- Moves each file to the correct folder  
- Supports custom categories

## Run the tool
```bash
python organizer.py
```

## Customize categories
```bash
json
{
    "pdf": "DOCUMENTS",
    "jpg": "IMAGES"
}
```