import logging
import os
from datetime import datetime
import sys

def setup_logger(name=None, log_level=logging.INFO, log_file=None):
    """
    Set up and configure logger for the automation suite
    
    Args:
        name (str): Logger name
        log_level: Logging level (default: INFO)
        log_file (str): Path to log file (optional)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if log_file and not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create logger
    logger = logging.getLogger(name or 'automation_suite')
    logger.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log file specified)
    if log_file:
        # Add timestamp to log file name
        if not log_file.startswith('logs/'):
            log_file = f"logs/{log_file}"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_function_logger(func):
    """
    Decorator to add logger to function with function-specific context
    """
    def wrapper(*args, **kwargs):
        logger = setup_logger(func.__name__)
        logger.debug(f"Function {func.__name__} called with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {func.__name__} failed with error: {str(e)}")
            raise
    return wrapper

# Pre-configured loggers
main_logger = setup_logger('automation_suite')
file_logger = setup_logger('file_organizer')
web_logger = setup_logger('web_scraper')
doc_logger = setup_logger('document_extractor')