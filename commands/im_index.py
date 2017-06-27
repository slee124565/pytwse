'''
TWSE SRC PAGE http://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html
'''

import requests
import json
from datetime import datetime, timedelta
import os
from .base import BaseCommand

SRC_URL = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={Ymd}&type={category}'


class ImIndex(BaseCommand):
    ''''''
    
    @classmethod
    def add_parser_argument(cls,parser):
        BaseCommand.add_parser_argument(parser)
        parser.add_argument('--category',
                                     help='[category] query field on page, default:%(default)s',
                                     default='ALLBUT0999'
                                     )
        parser.add_argument('--date',
                                 help='[date] query field on page; format:YYYY-MM-DD, default: today',
                                 default=datetime.today().strftime('%Y-%m-%d'))
        
    @classmethod
    def add_cmd_parser(cls,subparsers):
        ''''''
        cmd_parser = subparsers.add_parser(
            'im_index',
            help='http://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html')
        ImIndex.add_parser_argument(cmd_parser)
        return cmd_parser
            
    def __init__(self, args):
        ''''''
        super(ImIndex,self).__init__(args)
        setattr(self.args, 'date', datetime.strptime(self.args.date,'%Y-%m-%d'))
        self.logger.debug('ImIndex with args %s' % self.args)
    
    def _data_validate(self,twse_json):
        '''[u'alignsStyle3', u'alignsStyle2', u'alignsStyle1', u'fields4', u'data2', 
u'alignsStyle5', u'alignsStyle4', u'stat', u'subtitle5', u'subtitle4', u'subtitle1', 
u'params', u'fields2', u'fields3', u'fields1', u'data1', u'notes5', u'notes4', 
u'groups5', u'data5', u'data4', u'date', u'data3', u'fields5']
'''
        if len(twse_json.keys()) == 24:
            return True
        else:
            self.logger.warning('%s data_validate fail' % self.__class__.__name__)
            
    def run(self):
        ''''''
        renew_cache = False
        cached_file = os.path.join(self.args.cache_path,self.args.category+'.json')
        self.logger.debug('cached_file: %s' % cached_file)
        if self.args.cached and os.path.exists(cached_file):
            self.logger.info('read from cached file')
            with open(cached_file,'rb') as fh:
                twse_json = json.loads(fh.read())
        else:
            target_date = self.args.date
            max_try = 7
            count_try = 1
            while count_try <= max_try:        
                url = SRC_URL.format(Ymd=target_date.strftime('%Y%m%d'),
                                     category=self.args.category)
                self.logger.debug('download from twse with url: %s' % url)
                r = requests.get(url)
                twse_json = r.json()
                if not 'data5' in twse_json.keys() or not 'fields5' in twse_json.keys():
                    target_date = target_date - timedelta(days=1)
                    self.logger.warning('twse list date (%s) not exist, try previous day %s' % (
                        target_date.strftime('%Y-%m-%d'),count_try
                        ))
                    count_try += 1
                else:
                    break
            renew_cache = True
        
        self.logger.debug('twse json object keys (%s): %s' % (len(twse_json.keys()),
                                                              twse_json.keys()))
        if self._data_validate(twse_json) and renew_cache:
            with open(cached_file,'wb') as fh:
                fh.write(json.dumps(twse_json,indent=2))
            self.logger.debug('cache file renewed')
        
        self.logger.info('im_index command executed')
        self.twse_json = twse_json
        return twse_json
        
    def get_index(self):
        stock_id_list = []
        for entry in self.twse_json.get('data5'):
            stock_id_list.append(entry[:2]+entry[5:9])
        return stock_id_list
        
    def get_date(self):
        ''''''
        return datetime.strptime(self.twse_json.get('date'),'%Y%m%d').date()
        
        
        