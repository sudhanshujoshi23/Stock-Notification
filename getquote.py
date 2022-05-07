import nsepy as nse
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils

# Using the list of 50 companies present in Nifty50
list_nse_50_url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
df1 = pd.read_csv(list_nse_50_url)

# Fetching data from NSEPY and writing it to a dataframe
stock_data = pd.DataFrame()
for stock in df1['Symbol'].tolist():
    stock_info = []
    stock_info = nse.get_history(stock, start=datetime.today() - relativedelta(days=30), end=datetime.today())
    stock_data = stock_data.append(stock_info, sort=False)

line = utils.make_line_protocol(stock_data)
utils.push_to_influxdb(line)