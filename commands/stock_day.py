'''
TWSE SRC PAGE http://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html
'''

import logging
import argparse
import requests
import json
from datetime import datetime, timedelta
import os
from base import BaseCommand

SRC_URL = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Ymd}&stockNo={stock_no}'

class StockDay(BaseCommand):
    ''''''
    ARGS_DATE_FORMAT = '%Y-%m-%d'
    date_select = datetime.today().date()
    stock_no = '0050'
    read_cache = False
    
    @classmethod
    def get_cache_instance(cls,stock_no,date_select,debug=False):
        parser = argparse.ArgumentParser()
        StockDay.add_parser_argument(parser)
        argv = '--cached'
        if debug:
            argv += ' --debug'
        argv += ' --date_select %s' % date_select.strftime(StockDay.ARGS_DATE_FORMAT)
        argv += ' %s' % stock_no
        args = parser.parse_args(argv.split())
        worker = StockDay(args=args)
        worker.run()
        return worker
            
    def __init__(self, **argv):
        ''''''
        super(StockDay,self).__init__(**argv)
        #-> convert args.date to datetime.date object
        if argv.get('date_select'):
            self.date_select = argv.get('date_select')
        if argv.get('stock_no'):
            self.stock_no = argv.get('stock_no')
        if argv.get('read_cache'):
            self.read_cache = argv.get('read_cache')
        
        self.logger.debug('%s init with stock_no %s and date_select %s' % (self.__class__.__name__,
                                                                           self.stock_no,
                                                                           self.date_select)) 
        self.logger.debug('%s with cache_path %s' % (self.__class__.__name__,
                                                     self.cache_path))
        
    
    def _data_validate(self,twse_json):
        '''[u'stat', u'title', u'fields', u'notes', u'date', u'data']'''
        if len(twse_json.keys()) == 6:
            self.logger.debug('%s data_validate pass' % self.__class__.__name__)
            return True
        else:
            self.logger.warning('%s data_validate fail' % self.__class__.__name__)
            
    def _get_cache_file_path(self):
        ''''''
        cache_dir = os.path.join(self.cache_path,self.stock_no)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        cached_file = os.path.join(cache_dir,self.stock_no 
                                   + '_' + self.date_select.strftime('%Y%m%d') 
                                   +'.json')
        self.logger.debug('stock_no %s and date_select %s with cached_file: %s' % (
            self.stock_no, self.date_select, cached_file))
        return cached_file
        
    def run(self):
        ''''''
        renew_cache = False
        #-> define cache_file: 
        cached_file = self._get_cache_file_path()
        
        if self.read_cache and os.path.exists(cached_file):
            self.logger.info('read from cached file')
            with open(cached_file,'rb') as fh:
                twse_json = json.loads(fh.read())
        else:
            target_date = self.date_select
            max_try = 14
            count_try = 1
            while count_try <= max_try:        
                url = SRC_URL.format(Ymd=target_date.strftime('%Y%m%d'),
                                     stock_no=self.stock_no)
                self.logger.debug('download twse url: %s' % url)
                r = requests.get(url)
                twse_json = r.json()
                if not self._data_validate(twse_json):
                    target_date = target_date - timedelta(days=1)
                    self.logger.warning('twse stock date (%s) not exist, try previous day %s' % (
                        target_date.strftime('%Y-%m-%d'),count_try
                        ))
                    count_try += 1
                else:
                    break
            renew_cache = True
        
        self.logger.debug('fields: %s' % ','.join(
            n.encode('utf-8') for n in twse_json.get('fields')))
        if self._data_validate(twse_json) and renew_cache:
            with open(cached_file,'wb') as fh:
                fh.write(json.dumps(twse_json,indent=2))
            self.logger.debug('stock_no %s with date_select %s cache file renewed' % (
                self.stock_no,self.date_select))
        
        self.logger.info('stock_no %s with date_select %s read' % (self.stock_no,self.date_select))
        self.twse_json = twse_json
        return twse_json
        
    def get_data(self):
        return self.twse_json.get('data')
    
    def get_date(self):
        ''''''
        return datetime.strptime(self.twse_json.get('date'),'%Y%m%d').date()

if __name__ == '__main__':

    stock_0050 = StockDay()
    stock_0050.run()
    stock_0050.logger.debug('stock_no %s with date_select %s:' % (
        stock_0050.stock_no,stock_0050.date_select))
    for entry in stock_0050.get_data():
        stock_0050.logger.debug('%s' % entry)
        
    
    
    
    
    
    