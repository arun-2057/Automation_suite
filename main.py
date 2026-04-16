import os
import sys
import argparse

# Add the project root and utils to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir

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
        
        # Demo with sample files
        sample_files = [
            os.path.join(project_root, 'document_extractor', 'sample.txt'),
            os.path.join(project_root, 'document_extractor', 'sample.pdf')
        ]
        
        for sample_file in sample_files:
            if os.path.exists(sample_file):
                print(f"\n Analyzing: {sample_file}")
                text, stats = extractor.extract_from_file(sample_file)
                print(f"  - Words: {stats['word_count']}")
                print(f"  - Characters: {stats['char_count']}")
                print(f"  - Sentences: {stats['sentence_count']}")
                if 'page_count' in stats:
                    print(f"  - Pages: {stats['page_count']}")
                print(f"  - Top words: {[w[0] for w in stats['top_words'][:5]]}")
        
    except ImportError as e:
        logger.error(f"Failed to import document extractor: {e}")
        print(" Document extractor module not found")
        
    except Exception as e:
        logger.error(f"Error in document extractor demo: {e}")
        print(f" Error: {e}")

def run_file_organizer():
    """Run the file organizer tool"""
    from file_organizer.organizer import organize_files
    
    print("\n📁 File Organizer")
    print("-" * 40)
    
    # Get source directory
    source_dir = input("Enter source directory path (or press Enter for current dir): ").strip()
    if not source_dir:
        source_dir = os.getcwd()
    
    if not os.path.exists(source_dir):
        print(f"Error: Directory '{source_dir}' does not exist!")
        return
    
    # Get config file
    config_file = os.path.join(project_root, 'file_organizer', 'config.json')
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found!")
        return
    
    print(f"\nOrganizing files in: {source_dir}")
    print(f"Using config: {config_file}")
    
    try:
        organize_files(source_dir, config_file)
        print("\n✅ File organization completed!")
    except Exception as e:
        print(f"\n❌ Error organizing files: {e}")
        logger.error(f"File organizer error: {e}")


def run_web_scraper():
    """Run the web scraper tool"""
    from web_scraper.scraper import fetch_page, parse_headlines, save_json, save_csv
    from datetime import datetime
    
    print("\n🌐 Web Scraper")
    print("-" * 40)
    
    print("Choose a scraping option:")
    print("1. Scrape Hacker News headlines (default)")
    print("2. Custom URL scraping")
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == '2':
        url = input("Enter URL to scrape: ").strip()
        if not url:
            print("No URL provided. Aborting.")
            return
    else:
        url = "https://news.ycombinator.com/"
    
    print(f"\nScraping: {url}")
    
    try:
        html = fetch_page(url)
        headlines = parse_headlines(html)
        
        if not headlines:
            print("No headlines found!")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        json_file = f"headlines_{timestamp}.json"
        csv_file = f"headlines_{timestamp}.csv"
        
        save_json(headlines, json_file)
        save_csv(headlines, csv_file)
        
        print(f"\n✅ Successfully scraped {len(headlines)} headlines!")
        print(f"Saved to: {json_file} and {csv_file}")
        
    except Exception as e:
        print(f"\n❌ Error scraping: {e}")
        logger.error(f"Web scraper error: {e}")


def run_document_extractor():
    """Run the document extractor tool"""
    from document_extractor.extractor import DocumentExtractor
    
    print("\n📄 Document Extractor")
    print("-" * 40)
    
    extractor = DocumentExtractor()
    
    print("Choose an option:")
    print("1. Analyze sample files")
    print("2. Extract from custom file")
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == '1':
        document_extractor_demo()
    else:
        file_path = input("Enter file path: ").strip()
        if not file_path or not os.path.exists(file_path):
            print("Invalid file path!")
            return
        
        try:
            print(f"\nAnalyzing: {file_path}")
            text, stats = extractor.extract_from_file(file_path)
            
            print(f"\n📊 Statistics:")
            print(f"  - Words: {stats['word_count']}")
            print(f"  - Characters: {stats['char_count']}")
            print(f"  - Sentences: {stats['sentence_count']}")
            print(f"  - Paragraphs: {stats['paragraph_count']}")
            if 'page_count' in stats:
                print(f"  - Pages: {stats['page_count']}")
            print(f"  - File size: {stats['file_size_mb']:.2f} MB")
            
            print(f"\n🔤 Top 10 words:")
            for word, count in stats['top_words']:
                print(f"  - {word}: {count}")
            
            # Option to save extracted text
            save = input("\nSave extracted text? (y/n): ").strip().lower()
            if save == 'y':
                output_path = input("Enter output file path: ").strip()
                if output_path:
                    extractor.save_extracted_text(text, output_path)
                    print(f"✅ Text saved to: {output_path}")
                    
        except Exception as e:
            print(f"\n❌ Error extracting document: {e}")
            logger.error(f"Document extractor error: {e}")


def show_system_info():
    """Display system information"""
    from utils.helpers import get_system_info
    
    print("\n💻 System Information")
    print("-" * 40)
    
    info = get_system_info()
    print(f"Operating System: {info['system']} {info['release']}")
    print(f"Version: {info['version']}")
    print(f"Machine: {info['machine']}")
    print(f"Processor: {info['processor']}")
    print(f"Python Version: {info['python_version']}")
    print(f"\nProject Root: {project_root}")
    print(f"Current Directory: {os.getcwd()}")


def main():
    logger.info("Automation Suite started")
    
    # Your main menu code
    while True:
        print(f"\n{'='*50}")
        print(f"🤖 AUTOMATION SUITE - {format_timestamp()}")
        print(f"{'='*50}")
        print("1. 📁 File Organizer")
        print("2. 🌐 Web Scraper") 
        print("3. 📄 Document Extractor")
        print("4. 💻 System Info")
        print("5. Exit")
        
        choice = input("\nSelect tool (1-5): ").strip()
        
        if choice == '1':
            logger.info("File Organizer selected")
            run_file_organizer()
        elif choice == '2':
            logger.info("Web Scraper selected")
            run_web_scraper()
        elif choice == '3':
            logger.info("Document Extractor selected")
            run_document_extractor()
        elif choice == '4':
            logger.info("System Info selected")
            show_system_info()
        elif choice == '5':
            logger.info("Automation Suite exited")
            print("\nGoodbye! 👋")
            break
        else:
            logger.warning(f"Invalid menu choice: {choice}")
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()