
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
    def store_update_with_csv(cls, stock_no, csv_content):
        df_update = pd.read_csv(StringIO(u'{}'.format(csv_content)), index_col=['Date'], parse_dates=['Date'])

        stock_store_file = CSVStore.get_stock_store_file(stock_no)
        frames = []
        if os.path.exists(stock_store_file):
            df_origin = pd.read_csv(stock_store_file, index_col=['Date'], parse_dates=['Date'])
            frames.append(df_origin)
            count_origin, _ = df_origin.shape
            logger.debug('{} store_update_with_csv load exist stock csv, count {}'.format(
                cls.__name__, count_origin))
        else:
            count_origin = 0

        frames.append(df_update)
        stock_df = pd.concat(frames)

        count_1, _ = count_0, _ = stock_df.shape
        if len(frames) > 1:
            logger.debug('{} store_update_with_csv with drop_duplicates'.format(cls.__name__))
            stock_df = stock_df.reset_index().drop_duplicates('Date', keep='last').set_index('Date')
            count_1, _ = stock_df.shape

        if count_1 < count_0:
            logger.debug('{} store_update_with_csv {} drop duplicates {}'.format(
                cls.__name__, stock_no, (count_0-count_1)
            ))
        else:
            logger.debug('{} store_update_with_csv no duplicated found'.format(cls.__name__))

        tmp_file = '{}.tmp'.format(stock_store_file)
        stock_df.to_csv(tmp_file)
        os.rename(tmp_file, stock_store_file)
        count_final, _ = stock_df.shape
        logger.info('store_update_with_csv {} count {} with new {} final {}'.format(
            stock_no, count_origin, (count_1-count_origin), count_final))
        return stock_df

    @classmethod
    def store_get_dataframe(cls, stock_no):
        store_file = CSVStore.get_stock_store_file(stock_no)
        if os.path.exists(store_file):
            stock_df = pd.read_csv(store_file, index_col=['Date'], parse_dates=['Date'])
            logger.info('store_get_dataframe {} shape {}'.format(stock_no, stock_df.shape))
            return stock_df
        else:
            logger.warning('{} store_get_dataframe {} not exist'.format(cls.__name__, stock_no))
            return None


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
