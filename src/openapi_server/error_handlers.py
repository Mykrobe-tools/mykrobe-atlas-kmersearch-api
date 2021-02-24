import logging

logger = logging.getLogger(__name__)


def internal_server_error_handler(e):
    logger.error(e)