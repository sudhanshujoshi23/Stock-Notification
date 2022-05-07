import os
from urllib.error import HTTPError
import requests
from dotenv import load_dotenv
# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Load environment variables
load_dotenv()
token = os.getenv('DB_TOKEN')
host = os.getenv('DB_HOST')
org = os.getenv('DB_ORG')
bucket = os.getenv('DB_BUCKET')

# Function to make the line protocol for posting to influxDB
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
