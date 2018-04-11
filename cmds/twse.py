
from datetime import timedelta, datetime
import requests

import logging
logger = logging.getLogger(__name__)

SRC_URL = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Ymd}&stockNo={stock_no}'
DATE_FORMAT = '%Y-%m-%d'


def fetch_json(stock_no, tdate):
    logger.debug('twse fetch stock_no {} with target date {}'.format(stock_no, tdate))
    max_try = 14
    count_try = 1
    target_date = tdate
    twse_json = None
    while count_try <= max_try:
        url = SRC_URL.format(Ymd=target_date.strftime('%Y%m%d'),
                             stock_no=stock_no)
        logger.debug('twse fetch url: {}'.format(url))
        r = requests.get(url)
        twse_json = r.json()

        # validate twse_json object keys: [u'stat', u'title', u'fields', u'notes', u'date', u'data']
        logger.debug('twse fetch object keys: {}'.format(str(twse_json.keys())))
        if len(twse_json.keys()) != 6:
            logger.warning('twse fetch object keys validate fail, {}'.format(str(twse_json.keys())))
            target_date = target_date - timedelta(days=1)
            count_try += 1
            logger.warning('twse fetch retry count {}'.format(count_try))
        else:
            logger.debug('twse fetch success')
            logger.debug('twse fetch final url {}'.format(url))
            logger.debug('twse fetch final data count {}'.format(len(twse_json.get('data'))))
            break
            
        if count_try > max_try:
            logger.warning('twse fetch max retry exceed, break')
            twse_json = None
            break

    return twse_json


if __name__ == '__main__':

    # set logging
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    log_level = logging.DEBUG
    logger = logging.getLogger()
    logger.setLevel(log_level)

    fetch_json('2330', datetime.today())