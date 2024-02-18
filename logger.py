import logging
import datetime
from config import config

def logger():
    logger = logging.getLogger()
    logging.basicConfig(
        filename='logs/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_IP-'+config['IP-address-for-cam']+'_channel-'+config['channel-id-for-cam']+'.log',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    return logger

