# subscribe to bybit ws and input into db a row for each trade that has been executed.
# from dotenv import load_dotenv
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from pathlib import Path
# import json

# load_dotenv()
# KEY = os.environ.get("BYBIT_API_KEY")
# SECRET = os.environ.get("BYBIT_SECRET")

from pybit import WebSocket
from pprintpp import pprint
from models.trade import Trade, db
import pandas as pd

# query = Trade.select()
# pprint([trade.trade_id for trade in query])

# if 

# get 7 days worth of trades 
# from trades local file
# insert each trade into db.
base_path = Path(__file__).parent
days = ["2021-08-31", "2021-09-01", "2021-09-02", "2021-09-03", "2021-09-04", "2021-09-05", "2021-09-06"]
for day in days:
  day_path = (base_path / f"../data/trades/{day}").resolve()
  trades_for_day = pd.read_feather(day_path)

  # print(trades_for_day)
  trades_for_day = trades_for_day.rename(columns={"trdMatchID": "trade_id", "tickDirection": "tick_direction"})
  trades_for_day = trades_for_day.drop(['foreignNotional', 'grossValue', 'homeNotional', 'index', 'symbol'], axis=1)
  # print(trades_for_day)
  print(f"number of rows for day {day}: {len(trades_for_day.index)}")

  trades_dict = trades_for_day.to_dict('records')
  # pprint(trades_for_day.to_dict('records'))

  with db.atomic():
    for idx in range(0, len(trades_dict), 5000):
      Trade.insert_many(trades_dict[idx:idx+5000]).execute()