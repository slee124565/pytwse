
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os, json

from base import BaseCommand
from stock_day import StockDay

class StockUpdate(BaseCommand):
    ''''''
    stock_no = '0050'
    years = 3
    
    def __init__(self, **argv):
        ''''''
        super(StockUpdate,self).__init__(**argv)
        
        if argv.get('stock_no'):
            self.stock_no = argv.get('stock_no')
        if argv.get('years'):
            self.years = argv.get('years')
            
            
    def run(self):
        ''''''
        target_date = datetime.today() - relativedelta(years=self.years)
        stock_date = datetime.today()
        argv = {
            'date_select': stock_date,
            'stock_no': self.stock_no,
            'read_cache': True
            }
        stock_day = StockDay(**argv)
        while stock_date > target_date:
            self.logger.debug('run cmd %s' % str(stock_day))
            twse_json = stock_day.run()
            result_date = datetime.strptime(twse_json['date'],'%Y%m%d').date()
            result_data = twse_json['data']
            #-> check if there is previous download
            save_filename = os.path.join(self.get_stock_data_path(self.stock_no),
                                         '%s_%s.json' % (self.stock_no,result_date.strftime('%Y%m')))
            if os.path.exists(save_filename):
                with open(save_filename,'r') as fh:
                    prev_stock_data = json.loads(fh.read())
                    if len(prev_stock_data) == len(result_data):
                        self.logger.info('stock %s Ym %s already exist, stop updating' % 
                                          (self.stock_no,stock_date))
                        break
            #-> save twse download result json
            for entry in result_data:
                arr_ymd = entry[0].split('/')
                entry[0] = '%s/%s/%s' % (1911+int(arr_ymd[0]),arr_ymd[1],arr_ymd[2])
            with open(save_filename,'w') as fh:
                fh.write(json.dumps(result_data,indent=2))
            stock_date = datetime(stock_date.year,stock_date.month,1) - relativedelta(days=1)
            stock_day.date_select = stock_date
        
if __name__ == '__main__':
    
    stock_update = StockUpdate()
    stock_update.run()