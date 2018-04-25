

import argparse


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
