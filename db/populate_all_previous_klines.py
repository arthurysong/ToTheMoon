#! /usr/bin/python3

# ======= sibling imports =======
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# ======= sibling imports =======

# '''script to populate db w all available klines'''
# - START_TIMESTAMP is the earliest available time_stamp


import requests
from pathlib import Path
from pprintpp import pprint
from config.params import START_TIMESTAMP
import time
from models.kline import Kline, db

BYBIT_API = "https://api.bybit.com"
TIME_FRAME = 15 # 15 min interval
# FROM_TIMESTAMP = START_TIMESTAMP # this is the earliest valid timestamp avail in BYBITAPI
FROM_TIMESTAMP = 1633764600
SYMBOL = "BTCUSD"

t = FROM_TIMESTAMP

now = time.time()
total_seconds = now - FROM_TIMESTAMP
print(f'current time: {now}')
print(f'total seconds passed from START TIME ({FROM_TIMESTAMP}): {total_seconds}')
print(f'total fetch calls needed: {total_seconds / 180000}')
input("Press Enter to continue...")

while t < time.time():
  print(f'Fetching from timestamp {t}...')
  r = requests.get(f"{BYBIT_API}/v2/public/kline/list?symbol={SYMBOL}&interval={TIME_FRAME}&from={t}")
  json = r.json()
  t = json["result"][-1]["open_time"] + 900

  for kline in json["result"]:
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