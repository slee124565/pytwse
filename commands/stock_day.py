'''
TWSE SRC PAGE http://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html
'''

import requests
import json
from datetime import datetime, timedelta
import os
from .base import BaseCommand

SRC_URL = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={Ymd}&stockNo={stock_no}'

class StockDay(BaseCommand):
    ''''''
    ARGS_DATE_FORMAT = '%Y-%m-%d'
    
    @classmethod
    def add_parser_argument(cls,parser):
        BaseCommand.add_parser_argument(parser)
        parser.add_argument('--date_select',
                                 help='query field [date-select] on page, default:[today]',
                                 default=datetime.today().strftime(cls.ARGS_DATE_FORMAT))
        parser.add_argument('stock_no',
                            help='query field [stockNo] on page')
        
    @classmethod
    def add_cmd_parser(cls,subparsers):
        ''''''
        cmd_parser = subparsers.add_parser(
            'stock_day',
            help='http://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html')
    
        StockDay.add_parser_argument(cmd_parser)
        return cmd_parser
        
    def __init__(self, args):
        ''''''
        super(StockDay,self).__init__(args)
        #-> convert args.date to datetime.date object
        setattr(self.args, 'date_select', datetime.strptime(self.args.date_select,'%Y-%m-%d'))
        self.logger.debug('StockDay with args %s' % self.args)
    
    def _data_validate(self,twse_json):
        '''[u'stat', u'title', u'fields', u'notes', u'date', u'data']'''
        if len(twse_json.keys()) == 6:
            return True
        else:
            self.logger.warning('%s data_validate fail' % self.__class__.__name__)
            
    def _get_cache_file_path(self, stock_no, date_select):
        ''''''
        cache_dir = os.path.join(self.args.cache_path,stock_no)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        cached_file = os.path.join(cache_dir,stock_no 
                                   + '_' + date_select.strftime('%Y%m%d') 
                                   +'.json')
        self.logger.debug('cached_file: %s' % cached_file)
        return cached_file
        
    def run(self):
        ''''''
        renew_cache = False
        #-> define cache_file: 
        cached_file = self._get_cache_file_path(self.args.stock_no, self.args.date_select)
        
        if self.args.cached and os.path.exists(cached_file):
            self.logger.info('read from cached file')
            with open(cached_file,'rb') as fh:
                twse_json = json.loads(fh.read())
        else:
            target_date = self.args.date_select
            max_try = 7
            count_try = 1
            while count_try <= max_try:        
                url = SRC_URL.format(Ymd=target_date.strftime('%Y%m%d'),
                                     stock_no=self.args.stock_no)
                self.logger.debug('download from twse with url: %s' % url)
                r = requests.get(url)
                twse_json = r.json()
                if not 'data' in twse_json.keys() or not 'fields' in twse_json.keys():
                    target_date = target_date - timedelta(days=1)
                    self.logger.warning('twse stock date (%s) not exist, try previous day %s' % (
                        target_date.strftime('%Y-%m-%d'),count_try
                        ))
                    count_try += 1
                else:
                    break
            renew_cache = True
        
        self.logger.debug('twse json object keys (%s): %s' % (len(twse_json.keys()),
                                                              twse_json.keys()))
        self.logger.debug('fields: %s' % ','.join(
            n.encode('utf-8') for n in twse_json.get('fields')))
        if self._data_validate(twse_json) and renew_cache:
            with open(cached_file,'wb') as fh:
                fh.write(json.dumps(twse_json,indent=2))
            self.logger.debug('cache file renewed')
        
        self.logger.info('%s command executed' % self.__class__.__name__)
        self.twse_json = twse_json
        return twse_json
        
    def get_data(self):
        return self.twse_json.get('data')
    
    def get_date(self):
        ''''''
        return datetime.strptime(self.twse_json.get('date'),'%Y%m%d').date()

