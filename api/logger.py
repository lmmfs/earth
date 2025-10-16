import logging
import os


#LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_LEVEL = 'INFO'

# 2. Configure the basic logger
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str):
    return logging.getLogger(name)
