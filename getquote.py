import os
import nsepy as nse
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()
token = os.getenv('DB_TOKEN')
host = os.getenv('DB_HOST')
org = os.getenv('DB_ORG')
bucket = os.getenv('DB_BUCKET')

client = InfluxDBClient(url=host, token=token)
print(client.health())

write_api = client.write_api(write_options=SYNCHRONOUS)

data = ["INFY,stock=INFY Open=1554,High=1575,Low=1534"]
write_api.write(bucket, org, data)

