import logging
import os

from common.constants import Constants


class LoggerUtility:
    @staticmethod
    def set_level():
        log_format = '%(asctime)-15s %(levelname)s:%(message)s'
        logging.basicConfig(format=log_format)
        logger = logging.getLogger(Constants.LOGGER_NAME)

        try:
            log_level = os.environ(Constants.LOGGER_LOG_LEVEL_ENV_VAR)
        except Exception as e:
            log_level = Constants.LOGGER_DEFAULT_LOG_LEVEL

        logger.setLevel(logging.getLevelName(log_level))
        return True

    @staticmethod
    def log_info(message):
        logger = logging.getLogger(Constants.LOGGER_NAME)
        logger.info('%s', message)
        return True

    @staticmethod
    def log_error(message):
        logger = logging.getLogger(Constants.LOGGER_NAME)
        logger.error('%s', message)
        return True

    @staticmethod
    def log_warning(message):
        logger = logging.getLogger(Constants.LOGGER_NAME)
        logger.warning('%s', message)
        return True
