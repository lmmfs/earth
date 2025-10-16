import logging

from constants import LOG_LEVEL

#LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()


logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str):
    return logging.getLogger(name)
