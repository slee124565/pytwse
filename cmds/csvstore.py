
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
