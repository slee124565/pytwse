#!/usr/bin/env python

import argparse
import logging
import sys
from commands.im_index import ImIndex
from commands.stock_day import StockDay
import os
from datetime import datetime, date

class TWSE():
    _cached = True
    _im_index = None
    _stock_day = None
    
    def __init__(self, *args, **kwargs):
        ''''''
        self._cached = kwargs.get('cached') or True
        self.logger = kwargs.get('logger') or logging.getLogger(__name__)
        
    def _get_im_index_singleton(self):
        if self._im_index is None:
            parser = argparse.ArgumentParser()
            ImIndex.add_parser_argument(parser)
            if self._cached:
                argv = '--cached'
            if self.logger.getEffectiveLevel() <= logging.DEBUG:
                argv += ' --debug'
            args = parser.parse_args(argv.split())
            worker = ImIndex(args=args)
            worker.run()
            self._im_index = worker
        return self._im_index
    
    def _get_stock_day_singleton(self,stock_no,date_select=date.today()):
        if self._stock_day is None:
            parser = argparse.ArgumentParser()
            StockDay.add_parser_argument(parser)
            if self._cached:
                argv = '--cached'
            if self.logger.getEffectiveLevel() <= logging.DEBUG:
                argv += ' --debug'
            argv += ' --date_select %s' % date_select.strftime(StockDay.ARGS_DATE_FORMAT)
            argv += ' %s' % stock_no
            args = parser.parse_args(argv.split())
            worker = StockDay(args=args)
            worker.run()
            self._stock_day = worker
        return self._stock_day
            
    
    def get_index(self):
        ''''''
        im_index = self._get_im_index_singleton()
        return im_index.get_index()
        
    def get_index_report_date(self):
        im_index = self._get_im_index_singleton()
        return im_index.get_date()
    
    def get_stock(self,stock_no,date_select=date.today()):
        ''''''
        stock_day = self._get_stock_day_singleton(stock_no,date_select)
        return stock_day.get_data()

def _cmd_im_index_execute(args):
    ''''''
    worker = ImIndex(args=args)
    worker.run()
    
def _cmd_stock_day_execute(args):
    ''''''
    worker = StockDay(args=args)
    worker.run()
    
if __name__ == '__main__':
        
    #-> program parser start
    parser = argparse.ArgumentParser(
        description='TWSE Site (http://www.twse.com.tw/) Exchange Data Parser')

    subparsers = parser.add_subparsers(
        title='commands')
    
    #-> [im_index] command arguments
    im_index_parser = ImIndex.add_cmd_parser(subparsers)
    im_index_parser.set_defaults(func=_cmd_im_index_execute)
    
    #-> [stock_day] command arguments
    stock_day_parser = StockDay.add_cmd_parser(subparsers)
    stock_day_parser.set_defaults(func=_cmd_stock_day_execute)
    
    args = parser.parse_args()
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='[%(levelname)s]: %(message)s',
        level=log_level)

#     output = os.path.join(os.path.dirname(__file__),'data')
#     if not os.path.exists(output):
#         os.mkdir(output)
#     setattr(args,'data_path',output)
    
    args.func(args)
    
    
    
    