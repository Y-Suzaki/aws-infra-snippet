import json
import logging


def lambda_handler(event, context):
    format = logging.Formatter('%(asctime)s %(levelname)s %(error_code)s [%(module_name)s] %(message)s', '%Y-%m-%dT%H:%M:%SZ')
    logger = logging.getLogger()
    
    for handler in logger.handlers:
        handler.setFormatter(format)
    
    logger.setLevel(logging.DEBUG)
    logger.debug('debug log @@@', extra={'error_code':'0002', 'module_name':'external papa'})
    logger.info('info log @@@', extra={'error_code':'0002', 'module_name':'external papa'})
    logger.warning('warn log @@@', extra={'error_code':'0002', 'module_name':'external papa'})
    logger.error('error log @@@', extra={'error_code':'0002', 'module_name':'external papa'})
    logger.critical('critical log @@@', extra={'error_code':'0002', 'module_name':'external papa'})
