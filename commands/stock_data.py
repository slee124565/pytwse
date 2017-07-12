
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json, os

from base import BaseCommand
from stock_update import StockUpdate

class StockData(BaseCommand):
    ''''''
    stock_no = '0050'
    stock_data = []

    def __init__(self,**argv):
        
        super(StockData,self).__init__(**argv)
        
        if argv.get('stock_no'):
            self.stock_no = argv.get('stock_no')

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__,self.stock_no)
    
    
    def get_index_data(self):
        stock_data_path = self.get_stock_data_path(self.stock_no)
        self.logger.debug('stock %s data path %s' % (self.stock_no,stock_data_path))
        self.stock_data = []
        for f in os.listdir(stock_data_path):
            self.logger.debug('add stock data file %s' % f)
            with open(os.path.join(stock_data_path,f),'r') as fh:
                self.stock_data += json.loads(fh.read())
        
        self.logger.debug('stock %s get_index_data len %s' % (self.stock_no,len(self.stock_data)))
        sorted(self.stock_data, key=lambda x: x[0])
        
        return self.stock_data
        
        
if __name__ == '__main__':
    stock = StockData()
    stock.get_index_data()
    for entry in stock.stock_data[:10]:
        stock.logger.info(entry)
    stock.logger.info('......')
    for entry in stock.stock_data[-10:]:
        stock.logger.info(entry)
        