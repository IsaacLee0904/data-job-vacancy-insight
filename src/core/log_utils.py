import os
import sys
import logging
from logging.handlers import RotatingFileHandler

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    COLORS = {
        logging.DEBUG: Colors.BLUE,
        logging.INFO: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.RED + Colors.BOLD,
    }

    def format(self, record):
        # Get the color for this log level
        color = self.COLORS.get(record.levelno, '')
        
        # Format the message
        formatted = super().format(record)
        
        # Add color to console output (not to file)
        if hasattr(self, '_is_console') and self._is_console:
            return f"{color}{formatted}{Colors.END}"
        return formatted

def set_logger(level=logging.INFO):
    """
    Set up and initialize the logger with colored console output.
    
    Returns:
    - logger: logging.Logger
        Configured logger instance with file and colored console handlers.
    """
    # Get the current script name (without file extension)
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    
    # Create log file path
    log_directory = "/app/logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file_path = os.path.join(log_directory, f"{script_name}.log")

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # File handler for logs (no colors)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(level)
    file_format = ColoredFormatter(
        '%(asctime)s %(levelname)s - %(filename)s:%(lineno)d - %(message)s', 
        datefmt='%Y-%m-%dT%H:%M:%S%z'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Console handler for logs (with colors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = ColoredFormatter(
        '%(asctime)s %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%dT%H:%M:%S%z'
    )
    console_format._is_console = True  # Mark as console formatter
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger
