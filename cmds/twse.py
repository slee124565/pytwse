"""
    TWSE Utility Class Major Function

    * classmethods *


        - TWSE.fetch_json(stock_no, tdate, load_from_cached=True, saved=True)
        - TWSE.get_stock_csv(, stock_no, tdate, with_header=False)

"""
from datetime import timedelta, datetime, date
import requests
import os
import codecs
import json
import unittest
import logging
logger = logging.getLogger(__name__)
if os.environ.get('LOG_LEVEL', None):
    log_level = int(os.environ.get('LOG_LEVEL'))
else:
    log_level = logging.WARNING


class TWSE(object):
    SRC_URL = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Ymd}&stockNo={stock_no}'
    DATE_FORMAT = '%Y-%m-%d'
    DATA_FIELDS = ['Date', 'Volume', 'Value', 'Open', 'High', 'Low', 'Close', 'Change', 'Transaction']

    @classmethod
    def get_or_create_cache_dir(cls):
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'twse_cached')
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        return cache_dir

    @classmethod
    def get_cached_file_name(cls, stock_no, tdate):
        return '{}_{}.json'.format(stock_no, tdate.strftime('%Y%m'))

    @classmethod
    def get_csv_file_name(cls, stock_no, tdate):
        return '{}_{}.csv'.format(stock_no, tdate.strftime('%Y%m'))

    @classmethod
    def get_stock_cached_file_path(cls, stock_no, tdate):
        cached_file = TWSE.get_cached_file_name(stock_no, tdate)
        cache_dir = TWSE.get_or_create_cache_dir()
        return os.path.join(cache_dir, cached_file)

    @classmethod
    def analysis_twse_json(cls, twse_json, printer=logger.debug):
        printer('==')
        printer('twse_json analysis report:')
        printer('keys: {}'.format(twse_json.keys()))
        printer('stat: {}'.format(twse_json.get('stat', '')))
        printer(u'title: {}'.format(twse_json.get('title', '')))
        if twse_json.get('fields', None):
            printer(u'fields: {}'.format(','.join(f for f in twse_json.get('fields'))))
        else:
            printer(u'fields: {}'.format(twse_json.get('fields', '')))
        printer('date: {}'.format(twse_json.get('date', '')))
        if type(twse_json.get('data', '')) == list:
            printer('data count: {}'.format(len(twse_json.get('data'))))
        else:
            printer('data type: {}'.format(type(twse_json.get('data'))))

    @classmethod
    def load_from_cached(cls, stock_no, tdate):
        cached_file = TWSE.get_stock_cached_file_path(stock_no, tdate)
        if cached_file and os.path.exists(cached_file):
            with codecs.open(cached_file, encoding='utf8') as fh:
                return json.loads(fh.read())
        else:
            return None

    @classmethod
    def fetch_json(cls, stock_no, tdate, load_from_cached=True, saved=True):
        logger.debug('twse fetch stock_no {} with target date {}'.format(stock_no, tdate))
        cache_dir = TWSE.get_or_create_cache_dir()

        target_date = tdate
        twse_json = None
        cache_file = os.path.join(cache_dir, TWSE.get_cached_file_name(stock_no, target_date))

        if load_from_cached:
            if not os.path.exists(cache_file):
                logger.debug('stock cache file {} not exist'.format(os.path.basename(cache_file)))
                twse_json = None
            else:
                logger.debug('twse fetch from cached file: {}'.format(os.path.basename(cache_file)))
                with codecs.open(cache_file, 'rb', encoding='utf8') as fh:
                    twse_json = json.loads(fh.read())

        if twse_json is None:
            max_try = 14
            count_try = 1
            while count_try <= max_try:
                url = TWSE.SRC_URL.format(Ymd=target_date.strftime('%Y%m%d'),
                                          stock_no=stock_no)
                logger.debug('twse fetch url: {}'.format(url))
                r = requests.get(url)
                twse_json = r.json()
                if saved:
                    with codecs.open(cache_file, 'wb', encoding='utf8') as fh:
                        fh.write(json.dumps(twse_json, indent=2))

                # validate twse_json object keys: [u'stat', u'title', u'fields', u'notes', u'date', u'data']
                logger.debug('twse fetch object keys: {}'.format(str(twse_json.keys())))
                if len(twse_json.keys()) != 6:
                    logger.warning('twse fetch object keys validate fail, {}'.format(str(twse_json.keys())))
                    target_date = target_date - timedelta(days=1)
                    count_try += 1
                    logger.warning('twse fetch retry count {}'.format(count_try))
                else:
                    TWSE.analysis_twse_json(twse_json, logger.debug)
                    break

                if count_try > max_try:
                    logger.warning('twse fetch max retry exceed, break')
                    twse_json = None
                    break

        return twse_json

    @classmethod
    def get_revised_date(cls, str_date):
        arr_date = str_date.split('/')
        arr_date[0] = 1911 + int(arr_date[0])
        str_date = '-'.join(str(n) for n in arr_date)
        try:
            datetime.strptime(str_date, TWSE.DATE_FORMAT)
            return str_date
        except ValueError:
            return None

    @classmethod
    def get_stock_csv(cls, stock_no, tdate, with_header=False, saved=False):
        twse_json = TWSE.fetch_json(stock_no, tdate)
        if twse_json:
            lines = []
            if with_header:
                lines.append(','.join(n for n in TWSE.DATA_FIELDS))
            for rowdata in twse_json.get('data'):
                t_data = rowdata
                t_data[0] = TWSE.get_revised_date(t_data[0])
                lines.append(','.join('"{}"'.format(n) for n in t_data))
            stock_csv = '\n'.join(str(line) for line in lines)
        else:
            stock_csv = None

        if saved:
            csv_file_path = os.path.join(TWSE.get_or_create_cache_dir(),
                                         TWSE.get_csv_file_name(stock_no, tdate))
            with open(csv_file_path, 'w') as fh:
                if stock_csv:
                    fh.write(stock_csv)

        return stock_csv


class TWSETestBase(unittest.TestCase):
    stock_no = None
    stock_date = None
    tdate = None

    test_stock_no = '0050'
    test_tdate = date(2017, 6, 30)
    test_stock_data_len = 23
    test_default = False

    def setUp(self):
        if TWSETestBase.stock_no and TWSETestBase.stock_date:
            self.stock_no = TWSETestBase.stock_no
            self.stock_date = TWSETestBase.stock_date
            if self.stock_date:
                self.tdate = datetime.strptime(self.stock_date, TWSE.DATE_FORMAT)
        else:
            self.stock_no = self.test_stock_no
            self.tdate = self.test_tdate
            self.test_default = True

        logger.debug('test setUp with {}, {}'.format(self.stock_no, self.tdate))


class TestTwseCsv(TWSETestBase):

    def setUp(self):
        super(TestTwseCsv, self).setUp()
        self.twse_json = TWSE.fetch_json(self.stock_no, self.tdate)

    def test_get_stoc_csv_w_header(self):
        stock_csv_w_header = TWSE.get_stock_csv(self.stock_no, self.tdate, with_header=True)
        self.assertEqual(len(self.twse_json.get('data'))+1, len(stock_csv_w_header.split('\n')))

    def test_get_stoc_csv_wo_header(self):
        stock_csv_wo_header = TWSE.get_stock_csv(self.stock_no, self.tdate, with_header=False)
        self.assertEqual(len(self.twse_json.get('data')), len(stock_csv_wo_header.split('\n')))


class TestTwse(TWSETestBase):

    def setUp(self):
        super(TestTwse, self).setUp()

    def test_fetch_json_from_web(self):
        cached_file = TWSE.get_cached_file_name(self.stock_no, self.tdate)
        cached_file_path = os.path.join(TWSE.get_or_create_cache_dir(), cached_file)

        if os.path.exists(cached_file_path):
            os.remove(cached_file_path)
            logger.debug('cached file {} removed'.format(cached_file))

        #  exec test function
        twse_json = TWSE.fetch_json(self.stock_no, self.tdate, saved=True, load_from_cached=False)

        #  assert twse_json not None
        self.assertNotEqual(None, twse_json)
        #  assert cached file created
        self.assertEqual(True, os.path.exists(cached_file_path))
        #  assert twse_json['stat'] is 'OK'
        self.assertEqual('OK', twse_json.get('stat'))

        if self.test_default:
            #  assert twse_json data len 23
            self.assertEqual(self.test_stock_data_len, len(twse_json.get('data')))

    def test_analysis_cached_twse_json(self):
        cached_file_path = TWSE.get_stock_cached_file_path(self.stock_no, self.tdate)
        if not os.path.exists(cached_file_path):
            TWSE.fetch_json(self.stock_no, self.tdate, load_from_cached=False)
        twse_json = TWSE.load_from_cached(self.stock_no, self.tdate)
        self.assertNotEqual(None, twse_json)
        TWSE.analysis_twse_json(twse_json, logger.info)

    def test_fetch_json_if_cache_exist(self):
        stock_cached_file_path = TWSE.get_stock_cached_file_path(self.stock_no, self.tdate)
        if not os.path.exists(stock_cached_file_path):
            TWSE.fetch_json(self.stock_no, self.tdate, saved=True, load_from_cached=False)

        #  exec test function
        twse_json = TWSE.fetch_json(self.stock_no, self.tdate, saved=True, load_from_cached=True)
        self.assertNotEqual(None, twse_json)

    def test_fetch_json_if_cache_not_exist(self):
        stock_cached_file_path = TWSE.get_stock_cached_file_path(self.stock_no, self.tdate)
        if os.path.exists(stock_cached_file_path):
            os.remove(stock_cached_file_path)
        #  exec test function
        twse_json = TWSE.fetch_json(self.stock_no, self.tdate, load_from_cached=True)
        self.assertNotEqual(None, twse_json)


if __name__ == '__main__':

    # set logging
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # logger = logging.getLogger()
    logger.setLevel(log_level)
    #
    # TWSE.fetch_json('2330', datetime.today())

    import sys

    logger.debug('sys.argv: {}, {}'.format(sys.argv, len(sys.argv)))
    if len(sys.argv) > 2:
        try:
            stock_date = sys.argv[-1]
            stock_no = sys.argv[-2]
            datetime.strptime(stock_date, TWSE.DATE_FORMAT)
            int(stock_no)
            TWSETestBase.stock_date = sys.argv.pop()
            TWSETestBase.stock_no = sys.argv.pop()
        except ValueError:
            TWSETestBase.stock_date = None
            TWSETestBase.stock_no = None

    unittest.main()
