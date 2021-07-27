#! /usr/bin/python3
# for sibling imports
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import requests
from pathlib import Path
from pprintpp import pprint
from config.params import START_TIMESTAMP
import time

BYBIT_API = "https://api.bybit.com"
TIME_FRAME = 15 # 15 min interval
FROM_TIMESTAMP = START_TIMESTAMP # this is the earliest valid timestamp avail in BYBITAPI
SYMBOL = "BTCUSD"

base_path = Path(__file__).parent
file_path = (base_path / "../data/raw_klines_data.m").resolve()
raw_klines_data = open(file_path, "w")

klines = []
klines_objs = []
x = 0
t = FROM_TIMESTAMP

# interval is 900 or 15 * 60
# max len of result is 200
# so ... 200 * 900
# range of time should be 180000
# next time should be equal to last + 900 or first + 180900
# while x < 600:

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
  klines_objs.extend(json["result"])

  for kline in json["result"]:
    str = f'{kline["open_time"]} {kline["open"]} {kline["high"]} {kline["low"]} {kline["close"]} {kline["volume"]} {kline["turnover"]}'

    klines.append(str)

raw_klines_data.write("\n".join(klines))

# just checking the times of each kline..
# def get_timestamps(obj):
#   return obj["open_time"]

# pprint(list(map(get_timestamps, klines_objs)))