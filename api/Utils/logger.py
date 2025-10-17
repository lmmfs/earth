import logging

from api.Utils.constants import LOG_FILE, LOG_FORMAT, LOG_LEVEL

def setup_logging():
    """
    Sets up the logger according to the values inside constants.py
    """
    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
def get_logger(name: str):
    """
    Gets the logger instance 

    :param name: Specified name for the logger.
    :type db: str
    """
    return logging.getLogger(name)
