
from twse import TWSE

twse = TWSE()
stock_index = twse.get_index()
data_date = twse.get_index_report_date()
for entry in stock_index:
    print(entry)
print(data_date)
    