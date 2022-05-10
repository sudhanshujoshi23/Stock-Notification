import nsepy as nse
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils

Nifty50 = nse.get_history(symbol="NIFTY 50",
                            start=datetime.today()-relativedelta(months=1),
                            end=datetime.today(),
                            index=True
                        )

Nifty_50_PE = nse.get_index_pe_history(symbol='NIFTY', 
                                    start=datetime.today() - relativedelta(months=1),
                                    end = datetime.today()
                                )

Nifty = pd.concat([Nifty50, Nifty_50_PE], axis=1, join='inner')

# Prepare line protocol string and send to InfluxDB
line = utils.make_line_protocol_index(Nifty, 'Nifty')
utils.push_to_influxdb(line)

# Prepare data to be sent to telegram
Close = Nifty.iloc[-1]['Close']
PriceToEarnings = Nifty.iloc[-1]['P/E']
PriceToBook = Nifty.iloc[-1]['P/B']

data = f'Nifty \n Close Price - {Close} \n P/E - {PriceToEarnings} \n P/B - {PriceToBook}'
print(data)

utils.push_to_telegram(data)