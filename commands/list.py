'''
twse source url: http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20170622&type=ALLBUT0999
'''

import logging
import requests
import json
from datetime import datetime, timedelta
import os
import sys

SRC_URL = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={Ymd}&type=ALLBUT0999'
JSON_FILENAME = 'twse_list.json'

class List(object):
    ''''''
    
    
    def __init__(self,args=None,logger=None):
        self.args = args
        self.logger = logger or logging.getLogger(__name__)

    def run(self):
        ''''''
        self.logger.debug('list run with args: %s' % self.args)
        cached_file = os.path.join(self.args.data_path,JSON_FILENAME)
        if self.args.cached and  os.path.exists(cached_file):
            self.logger.debug('read from cached file')
            with open(cached_file,'rb') as fh:
                twse_json = json.loads(fh.read())
        else:
            target_date = datetime.today()
            max_try = 7
            count_try = 1
            while count_try <= max_try:        
                url = SRC_URL.format(Ymd=target_date.strftime('%Y%m%d'))
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

            if self.args.develop:
                with open(cached_file,'wb') as fh:
                    fh.write(json.dumps(twse_json,indent=2))
        
        self.logger.debug('twse_json keys: %s' % twse_json.keys())
        if 'data5' in twse_json.keys() and 'fields5' in twse_json.keys():
            stock_id_list = []
            fields = twse_json.get('fields5')
            self.logger.debug('%s' % ','.join(n.encode('utf-8') for n in fields[:2]+fields[5:9]))
            for entry in twse_json.get('data5'):
                self.logger.debug('%s' % ','.join(n.encode('utf-8') for n in entry[:2]+entry[5:9]))
                stock_id_list.append(entry[:2]+entry[5:9])
            return stock_id_list
        else:
            self.logger.debug('target members (data5, fields5) not in twse json keys: %s' % twse_json.keys())
            return []
