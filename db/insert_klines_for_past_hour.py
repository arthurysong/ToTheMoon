# get 4 klines for this hour
# if time is 10:05 
# get klines 10:00, 10:15, 10:30, 10:45
# record in the kline database
# will be run every at the 50th minute of every hour using cron_job_for_kline.py

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
from models.kline import Kline, db

import time
import requests
from datetime import datetime, timedelta

BYBIT_API = "https://api.bybit.com"
TIME_FRAME = 15 # 15 min interval

from datetime import datetime, timedelta

now = datetime.now()

def hour_rounder(ts):
    if any(part > 0 for part in [ts.minute, ts.second, ts.microsecond]):
        return ts.replace(second=0, microsecond=0, minute=0)
    else:
        return ts

# print(now)
# print(hour_rounder(now))
# print(datetime.timestamp(hour_rounder(now)))
FROM_TIMESTAMP = int(datetime.timestamp(hour_rounder(now))) # this is the earliest valid timestamp avail in BYBITAPI
SYMBOL = "BTCUSD"
r = requests.get(f"{BYBIT_API}/v2/public/kline/list?symbol={SYMBOL}&interval={TIME_FRAME}&from={FROM_TIMESTAMP}")
print(r.json())

for kline in r.json()['result']:
    print(kline)
    kline, created = Kline.get_or_create(
        open_time = kline['open_time'],
        defaults={
            'open': kline['open'], 
            'high': kline['high'],
            'low': kline['low'],
            'close': kline['close'],
            'volume': kline['volume'],
            'turnover': kline['turnover']
        }
    )

# run through each kline and insert into db.