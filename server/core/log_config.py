import logging
import sys

def setup_logging():
    """
    Configures the logging for the application.
    """
    # Create a logger
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.DEBUG)

    # Create a handler to print to the console (stdout)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# Create a logger instance to be imported by other modules
logger = setup_logging()