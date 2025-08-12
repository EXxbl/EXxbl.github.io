import logging
import datetime
from config.settings import data_path
from logging import getLogger
from concurrent_log_handler import ConcurrentRotatingFileHandler


def record_log(log_name=''):
    logger = getLogger()
    formatter_str = '%(asctime)s [pid:%(process)d] [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
    now = datetime.datetime.now().strftime('%Y%m%d')
    formatter = logging.Formatter(formatter_str)
    logger.handlers.clear()
    if not logger.handlers:
        error_logfile = data_path + '/{}-{}-error.log'.format(log_name,now)
        error_handler = ConcurrentRotatingFileHandler(error_logfile, "a", 1024 * 1024 * 40, 5, 'utf-8')
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        info_logfile = data_path + '/{}-{}-info.log'.format(log_name,now)
        info_handler = ConcurrentRotatingFileHandler(info_logfile, "a", 1024 * 1024 * 40, 5, 'utf-8')
        info_handler.setFormatter(formatter)
        info_handler.setLevel(logging.INFO)
        debug_logfile = data_path + '/{}-{}-debug.log'.format(log_name,now)
        debug_handler = ConcurrentRotatingFileHandler(debug_logfile, "a", 1024 * 1024 * 40, 5, 'utf-8')
        debug_handler.setFormatter(formatter)
        debug_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.INFO)
        logger.addHandler(error_handler)
        logger.addHandler(info_handler)
        logger.addHandler(debug_handler)
    return logger
