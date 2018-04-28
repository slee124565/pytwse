

import argparse
from pandas import DataFrame

class CMDBase(object):

    arg_stock_no = 'stock_no'

    def __str__(self):
        return '{}'.format(self.__class__.__name__)

    # -- common args functions for all CMDBase
    @classmethod
    def get_base_parser(cls):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False)

        parser.add_argument(
            '--debug',
            action='store_true',
            help='print debug message',
            default=False)
        return parser

    @classmethod
    def add_parser_arg_stock_no(cls, parser):
        parser.add_argument(
            cls.arg_stock_no,
            type=str,
            help='stock no.')


class StockInfo(object):
    stock_no = None
    df = None  # dataframe object

    def __init__(self, stock_no):
        self.stock_no = str(stock_no)

    def __str__(self):
        return '\{{}\} (count: {}, {} - {})'.format(
            self.stock_no, self.row_count(), self.date_since(), self.date_last())

    def date_since(self):
        if type(self.df) is DataFrame:
            return self.df.index[0].date()
        else:
            return None

    def date_last(self):
        if type(self.df) is DataFrame:
            return self.df.index[-1].date()
        else:
            return None

    def row_count(self):
        if type(self.df) is DataFrame:
            return self.df.shape[0]
        else:
            return None