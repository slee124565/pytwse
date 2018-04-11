

import logging
logger = logging.getLogger(__name__)


def save_twse_data(stock_no, twse_data):
    logger.debug('save_twse_data({}, {})'.format(stock_no, twse_data))
