import logging
import os
from logging.handlers import TimedRotatingFileHandler

if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler('logs/logs.txt', when='midnight', interval=1, backupCount=7, encoding='utf-8')
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
