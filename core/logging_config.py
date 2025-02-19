import logging
import sys

def setup_logging():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create file handler which logs even debug messages
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to the handlers
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent logs from being propagated to the root logger
    logger.propagate = False

    return logger 