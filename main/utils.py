import os
from urllib.error import HTTPError
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
token = os.getenv('DB_TOKEN')
host = os.getenv('DB_HOST')
org = os.getenv('DB_ORG')
bucket = os.getenv('DB_BUCKET')

# Function to make the line protocol for posting stock data to influxDB
def make_line_protocol(df1):
    data = []
    for index,row in df1.iterrows():
        date, open, high, low, close, vwap, volume, percentdeliverable = index, row['Open'], row[
            'High'], row['Low'], row['Close'], row['VWAP'], row['Volume'], row['%Deliverble']
        line_protocol_string = ''
        line_protocol_string+=f'Stocks,'
        line_protocol_string+=f'symbol={row["Symbol"]} ' 
        line_protocol_string += f'Open={open},High={high},Low={low},Close={close},VWAP={vwap},Volume={volume},Delivery={percentdeliverable} '
        line_protocol_string+=str(int(datetime.strptime(str(date),'%Y-%m-%d').timestamp()))
        data.append(line_protocol_string)
    return data

# Function to make the line protocol for posting index data to influxDB
def make_line_protocol_index(df1, IndexSymbol):
    data = []
    for index,row in df1.iterrows():
        date, close, price_to_earnigs, price_to_book, dividend_yield = index, row['Close'], row['P/E'], row[
            'P/B'], row['Div Yield']
        line_protocol_string = ''
        line_protocol_string+=f'Index,'
        line_protocol_string+=f'symbol={IndexSymbol} ' 
        line_protocol_string += f'Close={close},PE={price_to_earnigs},PB={price_to_book},DividendY={dividend_yield} '
        line_protocol_string+=str(int(datetime.strptime(str(date),'%Y-%m-%d').timestamp()))
        data.append(line_protocol_string)
    return data

# Calling the influxDB API to post data
def push_to_influxdb(data):
    for line in data:
        try:
            response = requests.post(
                url=f"{host}/api/v2/write",
                data=line,
                params={
                    'bucket': bucket,
                    'org': org,
                    'precision': 's',
                    },
                headers={
                    'Authorization': f'Token {token}',
                    'Content-Type' : 'text/plain'
                }
            )
        except HTTPError:
            print("Unsuccessful")

# Function to push data to telegram channel.
def push_to_telegram(data):
    query_params = {
                    'chat_id': '@botnify',
                    'text': f'{data}'
                    }

    response = requests.get(
        url = "https://api.telegram.org/bot5306794126:AAHwbtgRCl-u4MFEbOxZAzH5KSLf0x6prM4/sendMessage",
        params = query_params, 
    )
