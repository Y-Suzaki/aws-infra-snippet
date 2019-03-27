from logger.lambda_json_logger import LambdaJsonLogger


def lambda_handler(event, context):
    logger = LambdaJsonLogger.get_logger('DEBUG')
    logger.info('lambda start.')
    logger.info('lambda end.')

    return 'OK'
