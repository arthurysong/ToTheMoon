# subscribe to bybit ws and input into db a row for each trade that has been executed.
from dotenv import load_dotenv
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import json

load_dotenv()
KEY = os.environ.get("BYBIT_API_KEY")
SECRET = os.environ.get("BYBIT_SECRET")

from pybit import WebSocket
from pprintpp import pprint
from models.trade import Trade, db

subs = [
    'orderBookL2_25.BTCUSD',
    'instrument_info.100ms.BTCUSD',
    'instrument_info.100ms.ETHUSD',
    'trade.BTCUSD'
]

ws = WebSocket(
    endpoint='wss://stream.bybit.com/realtime', 
    subscriptions=subs, 
    api_key=KEY,
    api_secret=SECRET
)

while True:
  response = ws.fetch('trade.BTCUSD')
  if response:
    # pprint(response)

    mapped_response = list(map(lambda x: {
      'timestamp': x['trade_time_ms']/1000,
      'side': x['side'],
      'size': x['size'],
      'price': x['price'],
      'tick_direction': x['tick_direction'],
      'trade_id': x['trade_id']
    }, response))

    pprint(mapped_response)

    with db.atomic():
      for idx in range(0, len(mapped_response), 100):
        Trade.insert_many(mapped_response[idx:idx+100]).execute()