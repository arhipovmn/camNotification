import logging
from config import config

def logger():
    logger = logging.getLogger()
    logging.basicConfig(
        filename='logs/camNotification.log',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    return logger

