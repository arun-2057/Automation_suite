import os
import sys

# Add the project root and utils to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) if os.path.basename(current_dir) != 'automation_suite' else current_dir

# Add both project root and utils to path
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'utils'))

try:
    from utils.logger import setup_logger, get_function_logger
    from utils.helpers import ConfigManager, get_file_size, format_timestamp
except ImportError:
    # Fallback: try direct import
    try:
        from logger import setup_logger, get_function_logger
        from helpers import ConfigManager, get_file_size, format_timestamp
    except ImportError as e:
        print(f" Import error: {e}")
        print(" Make sure you're running from the project root directory")
        sys.exit(1)

# Initialize logger and config
logger = setup_logger()
config = ConfigManager()

@get_function_logger
def document_extractor_demo():
    """Demo function using the new utils"""
    logger.info("Starting document extractor demo")
    
    # Your existing code here, now with logging
    print(f"Current timestamp: {format_timestamp()}")
    
    # Add your document extractor logic here
    try:
        from document_extractor.extractor import DocumentExtractor
        logger.info("Document extractor imported successfully")
        print(" Document extractor is ready!")
        
        # Example usage
        extractor = DocumentExtractor()
        print(" Document Extractor initialized")
        
    except ImportError as e:
        logger.error(f"Failed to import document extractor: {e}")
        print(" Document extractor module not found")
        
    except Exception as e:
        logger.error(f"Error in document extractor demo: {e}")
        print(f" Error: {e}")

def main():
    logger.info("Automation Suite started")
    
    # Your main menu code
    while True:
        print(f"\n Automation Suite - {format_timestamp()}")
        print("1. File Organizer")
        print("2. Web Scraper") 
        print("3. Document Extractor")
        print("4. System Info")
        print("5. Exit")
        
        choice = input("\nSelect tool (1-5): ").strip()
        
        if choice == '1':
            logger.info("File Organizer selected")
            print("📁 File Organizer - Coming soon!")
            # File organizer functionality
            pass
        elif choice == '2':
            logger.info("Web Scraper selected")
            print("🌐 Web Scraper - Coming soon!")
            # Web scraper functionality  
            pass
        elif choice == '3':
            logger.info("Document Extractor selected")
            document_extractor_demo()
        elif choice == '4':
            logger.info("System Info selected")
            print("\n System Information:")
            print(f"Project Root: {project_root}")
            print(f"Python Path: {sys.executable}")
            print(f"Current Directory: {os.getcwd()}")
        elif choice == '5':
            logger.info("Automation Suite exited")
            print("Goodbye!")
            break
        else:
            logger.warning(f"Invalid menu choice: {choice}")
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()