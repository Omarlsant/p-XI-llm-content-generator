import logging
import sys
from core.config import settings

def setup_logging() -> logging.Logger:
    """
    Configures application logging governed by environment settings.
    """
    logger = logging.getLogger("api_logger")
    
    # Determine level from settings, default to INFO if invalid
    level_name = getattr(settings, "LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(log_level)

    # Avoid duplicate handlers if setup_logging is called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        for handler in logger.handlers:
            handler.setLevel(log_level)

    return logger

# Create a logger instance to be imported by other modules
logger = setup_logging()
