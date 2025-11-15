import os
import sys
import json
import shutil
from datetime import datetime
import hashlib
import requests
from pathlib import Path
import mimetypes

def get_file_size(file_path):
    """Get human-readable file size"""
    size_bytes = os.path.getsize(file_path)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def get_file_hash(file_path, algorithm='md5'):
    """Calculate file hash"""
    hash_func = getattr(hashlib, algorithm)()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def create_directory(path):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False

def safe_delete(file_path):
    """Safely delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
    return False

def read_json(file_path):
    """Safely read JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file {file_path}: {e}")
        return None

def write_json(data, file_path, indent=2):
    """Safely write data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing JSON file {file_path}: {e}")
        return False

def get_file_extension(file_path):
    """Get file extension with dot"""
    return Path(file_path).suffix.lower()

def get_file_type(file_path):
    """Get file type category"""
    extension = get_file_extension(file_path)
    
    file_types = {
        # Images
        '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
        '.bmp': 'image', '.svg': 'image', '.webp': 'image', '.ico': 'image',
        '.tiff': 'image', '.tif': 'image',
        
        # Documents
        '.pdf': 'document', '.doc': 'document', '.docx': 'document',
        '.txt': 'document', '.rtf': 'document', '.md': 'document',
        '.log': 'document',
        
        # Spreadsheets
        '.xls': 'spreadsheet', '.xlsx': 'spreadsheet', '.csv': 'spreadsheet',
        
        # Presentations
        '.ppt': 'presentation', '.pptx': 'presentation',
        
        # Archives
        '.zip': 'archive', '.rar': 'archive', '.tar': 'archive',
        '.gz': 'archive', '.7z': 'archive',
        
        # Audio
        '.mp3': 'audio', '.wav': 'audio', '.flac': 'audio', '.aac': 'audio',
        '.ogg': 'audio', '.m4a': 'audio',
        
        # Video
        '.mp4': 'video', '.avi': 'video', '.mov': 'video', '.mkv': 'video',
        '.wmv': 'video', '.flv': 'video',
        
        # Code
        '.py': 'code', '.js': 'code', '.html': 'code', '.css': 'code',
        '.java': 'code', '.cpp': 'code', '.c': 'code', '.php': 'code',
        '.json': 'code', '.xml': 'code',
    }
    
    return file_types.get(extension, 'other')

def download_file(url, destination):
    """Download file from URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"Error downloading file from {url}: {e}")
        return False

def format_timestamp(timestamp=None):
    """Format timestamp for consistent use across tools"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d_%H-%M-%S")

def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """Create terminal progress bar"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    
    # Print new line on completion
    if iteration == total:
        print()

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_url(url):
    """Basic URL validation"""
    import re
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None

def count_files(directory, file_extension=None):
    """Count files in directory, optionally filtered by extension"""
    try:
        if file_extension:
            return len([f for f in os.listdir(directory) 
                       if f.endswith(file_extension) and os.path.isfile(os.path.join(directory, f))])
        else:
            return len([f for f in os.listdir(directory) 
                       if os.path.isfile(os.path.join(directory, f))])
    except FileNotFoundError:
        return 0

def get_system_info():
    """Get basic system information"""
    import platform
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version()
    }

class ConfigManager:
    """Manage configuration files for the automation suite"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'file_organizer': {
                'default_source': './downloads',
                'default_destination': './organized_files',
                'file_categories': {
                    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.md'],
                    'spreadsheets': ['.xls', '.xlsx', '.csv'],
                    'presentations': ['.ppt', '.pptx'],
                    'archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
                    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
                    'video': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'],
                    'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php']
                }
            },
            'web_scraper': {
                'timeout': 30,
                'user_agent': 'Mozilla/5.0 Automation Suite',
                'max_retries': 3
            },
            'document_extractor': {
                'supported_formats': ['.pdf', '.txt', '.md', '.log'],
                'max_file_size_mb': 50
            },
            'logging': {
                'level': 'INFO',
                'file': 'automation_suite.log'
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge with default config
                    return self._merge_configs(default_config, user_config)
            except Exception as e:
                print(f"Error loading config file: {e}. Using default configuration.")
        
        return default_config
    
    def _merge_configs(self, default, user):
        """Recursively merge user config with default"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, section, key=None, default=None):
        """Get configuration value"""
        if section not in self.config:
            return default
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key, default)
    
    def set(self, section, key, value):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False

# Global config instance
config = ConfigManager()