
from io import StringIO
import pandas as pd
from datetime import datetime, date
from twse import TWSE
import unittest
import os
import logging
logger = logging.getLogger(__name__)
if os.environ.get('LOG_LEVEL', None):
    log_level = int(os.environ.get('LOG_LEVEL'))
else:
    log_level = logging.WARNING


class CSVStore(object):

    def __str__(self):
        return '{}'.format(self.__class__.__name__)

    @classmethod
    def get_store_path(cls):
        store_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csvstore')
        if not os.path.exists(store_path):
            logger.debug('{} store_path not exist, creating {} ...'.format(cls.__name__, store_path))
            os.mkdir(store_path)
        return store_path

    @classmethod
    def get_stock_store_file(cls, stock_no):
        stock_store_file = os.path.join(CSVStore.get_store_path(), '{}.csv'.format(stock_no))
        if os.path.exists(stock_store_file):
            logger.debug('stock store file {} not exist'.format(stock_store_file))
        return stock_store_file

    @classmethod
    def update_stock_store(cls, stock_no, csv_content):
        df_update = pd.read_csv(StringIO(u'{}'.format(csv_content)), index_col=['Date'], parse_dates=['Date'])

        stock_store_file = CSVStore.get_stock_store_file(stock_no)
        frames = []
        if os.path.exists(stock_store_file):
            df_origin = pd.read_csv(stock_store_file, index_col=['Date'], parse_dates=['Date'])
            frames.append(df_origin)
            count_origin, _ = df_origin.shape
        else:
            count_origin = 0

        frames.append(df_update)
        stock_df = pd.concat(frames)

        count_1, _ = count_0, _ = stock_df.shape
        if len(frames) > 1:
            count_0, _ = stock_df.shape
            stock_df.drop_duplicates(keep='last', inplace=True)

        if count_1 < count_0:
            logger.debug('{} update_stock_store {} drop duplicates {}'.format(
                cls.__name__, stock_no, (count_1-count_0)
            ))

        tmp_file = '{}.tmp'.format(stock_store_file)
        stock_df.to_csv(tmp_file)
        os.rename(tmp_file, stock_store_file)
        count_final, _ = stock_df.shape
        logger.info('update_stock_store {} count {} with new {} final {}'.format(
            stock_no, count_origin, (count_1-count_origin), count_final))
        return stock_df

    @classmethod
    def get_revised_date(cls, str_date):
        arr_date = str_date.split('/')
        arr_date[0] = 1911 + int(arr_date[0])
        return '-'.join(str(n) for n in arr_date)

    @classmethod
    def save_stock_twse_json(cls, stock_no, twse_json):
        twse_data = twse_json.get('data')
        for rowdata in twse_data:
            rowdata[0] = CSVStore.get_revised_date(rowdata[0])


class TestCSVStore(unittest.TestCase):
    stock_no = None
    stock_date = None
    tdate = None

    test_stock_no = '0050'
    test_tdate = date(2017, 6, 30)
    test_default = False

    def setUp(self):
        if TestCSVStore.stock_no and TestCSVStore.stock_date:
            self.stock_no = TestCSVStore.stock_no
            self.stock_date = TestCSVStore.stock_date
            if self.stock_date:
                self.tdate = datetime.strptime(self.stock_date, TWSE.DATE_FORMAT)
        else:
            self.stock_no = self.test_stock_no
            self.tdate = self.test_tdate
            self.test_default = True

        logger.debug('test setUp with {}, {}'.format(self.stock_no, self.tdate))

    def test_get_revised_date(self):
        twse_json = TWSE.fetch_json(self.stock_no, self.tdate)
        self.assertNotEqual(None, twse_json)

        twse_data = twse_json.get('data')
        self.assertNotEqual(None, twse_json.get('data'))

        for rowdata in twse_data:
            revised_date_str = CSVStore.get_revised_date(rowdata[0])
            self.assertEqual(datetime, type(datetime.strptime(revised_date_str, TWSE.DATE_FORMAT)))


if __name__ == '__main__':

    #  set logging
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    logger.setLevel(log_level)

    import sys

    logger.debug('sys.argv: {}, len: {}'.format(sys.argv, len(sys.argv)))

    if len(sys.argv) > 1:
        TestCSVStore.stock_no = sys.argv.pop()

    unittest.main()
