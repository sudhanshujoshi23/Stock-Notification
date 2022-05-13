import nsepy as nse
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils

NiftyM100 = nse.get_history(symbol="NIFTY Midcap 100",
                            start=datetime.today()-relativedelta(months=1),
                            end=datetime.today(),
                            index=True
                        )

Nifty_MidCap_100PE = nse.get_index_pe_history(symbol='NIFTY MIDCAP 100', 
                                    start=datetime.today() - relativedelta(months=1),
                                    end = datetime.today()
                                )


Nifty_MidCap = pd.concat([NiftyM100, Nifty_MidCap_100PE], axis=1, join='inner')

# Prepare line protocol string and send to InfluxDB
line = utils.make_line_protocol_index(Nifty_MidCap, 'Nifty Midcap')
utils.push_to_influxdb(line)

# Prepare data to be sent to telegram
Close = Nifty_MidCap.iloc[-1]['Close']
PriceToEarnings = Nifty_MidCap.iloc[-1]['P/E']
PriceToBook = Nifty_MidCap.iloc[-1]['P/B']

data = f'Nifty Midcap 100 \n Close Price - {Close} \n P/E - {PriceToEarnings} \n P/B - {PriceToBook}'
print(data)

utils.push_to_telegram(data)