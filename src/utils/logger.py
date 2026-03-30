"""
Logging configuration for Alumni Data Extractor
"""
import logging
import os
from datetime import datetime


def setup_logger(name, log_level=logging.INFO):
    """
    Setup logger configuration
    
    Args:
        name (str): Logger name
        log_level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    
    # Create logs directory if it doesn't exist
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Check if logger already has handlers to avoid duplicates
    if logger.hasHandlers():
        return logger
    
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    
    # Create file handler
    log_file = os.path.join(logs_dir, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to handlers
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger


# Create application logger
app_logger = setup_logger('alumni_extractor')
