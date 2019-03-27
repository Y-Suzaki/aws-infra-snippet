import time
import traceback
import json
from logging import getLogger, Formatter


class LambdaJsonLogger:
    @staticmethod
    def get_logger(level):
        return LambdaJsonLogger(level)

    def __init__(self, level):
        self.logger = getLogger()
        self.logger.setLevel(level)

        self.formatter = Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "error_code": "%(error_code)s", "msg": "%(msg)s", "request_id": "%(aws_request_id)s"}',
            '%Y-%m-%dT%H:%M:%SZ')
        self.formatter.converter = time.gmtime

        self.formatter_exeception = Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "error_code": "%(error_code)s", "msg": "%(msg)s", "request_id": "%(aws_request_id)s", "exception": %(exception)s}',
            '%Y-%m-%dT%H:%M:%SZ')
        self.formatter_exeception.converter = time.gmtime
        self.logger.handlers[0].setFormatter(self.formatter)

    def debug(self, msg, error_code='-'):
        self.logger.debug(msg, extra={'error_code': error_code})

    def info(self, msg, error_code='-'):
        self.logger.info(msg, extra={'error_code': error_code})

    def error(self, msg, error_code):
        self.logger.error(msg, extra={'error_code': error_code})

    def exception(self, msg, error_code):
        self.logger.handlers[0].setFormatter(self.formatter_exeception)
        exception = json.dumps(traceback.format_exc().splitlines())
        self.logger.error(msg, extra={'error_code': error_code, 'exception': exception})
        self.logger.handlers[0].setFormatter(self.formatter)
