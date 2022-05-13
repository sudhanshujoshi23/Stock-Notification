import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
load_dotenv()

client = influxdb_client.InfluxDBClient(
    url=os.environ['DB_HOST'],
    token=f'Token {os.environ["DB_TOKEN"]}',
    org=os.environ['DB_ORG']
)

# print(client.health())

query_api = client.query_api()

# Base Flux Query 

base_query = 'from(bucket: "stocks") \
  |> range(start: -150d) \
  |> filter(fn: (r) => r["symbol"] == "{0}") \
  |> filter(fn: (r) => r["_field"] == "Close") \
  |> drop(columns: ["_start", "_stop", "_measurement"]) \
  |> map(fn: (r) => ({{ r with Close: float(v: r._value) }}))   \
  |> movingAverage(n: {1}) \
  |> last()'

stock_universe_query = 'import "influxdata/influxdb/schema" \
                        schema.tagValues(bucket: "stocks", tag: "symbol")'

tag_values = query_api.query(org=os.environ['DB_ORG'], query=stock_universe_query)

stock_universe = []
for tag in tag_values:
  for record in tag.records:
    stock_universe.append(record.values.get('_value'))

def cross_sma50_filter():
    # TODO: Filter stocks that have crossed SMA50 with
    # deliverable volume greater than avg deliverable volume in past 30 days
    # Volume Traded on Last Day is higher than avg volume in the past 30 dayss       

    botnify_json = {'stocks': ['LTP', 'SMA50']}
    for stocks in stock_universe:
        query_api.query(org=os.environ['DB_ORG'], query=base_query.format(stocks,50))
        # if record.values.get('Close') > record.values.get('_value'):
        #     botnify_json[stocks] = [record.values.get('Close'), record.values.get('_value')]
    return botnify_json

def cross_sma100_filter():
    pass

def break_sma50_filter():
    pass

def break_sma100_filter():
    pass

def golden_cross_filter():
    pass

def death_cross_filter():
    pass