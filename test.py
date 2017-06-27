
import logging
from twse import TWSE

logging.basicConfig(level=logging.DEBUG)
twse = TWSE()
# stock_index = twse.get_index()
# data_date = twse.get_index_report_date()
# for entry in stock_index:
#     print(entry)
# print(data_date)
    
stock = twse.get_stock('0050')
for entry in stock:
    print(entry)
