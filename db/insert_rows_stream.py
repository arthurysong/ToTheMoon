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
from models.trade import Trade

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
    pprint(response)

    for trade in response:
      # if not Trade.get_or_none(
      #   trade_id=trade['trade_id']
      # ):
      timestamp = trade['trade_time_ms'] / 1000
      Trade.get_or_create(
        timestamp=timestamp,
        side=trade['side'],
        size=trade['size'],
        price=trade['price'],
        tick_direction=trade['tick_direction'],
        trade_id=trade['trade_id']
      )