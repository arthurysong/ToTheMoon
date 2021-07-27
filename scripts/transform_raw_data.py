#! /usr/bin/python3

# for sibling imports
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.data_mutations import raw_to_nn_data, sets_to_grouped_sets
from utils.point_of_control import calc_point_of_control
from config.params import TOTAL_KLINES, SET_INTERVAL
from pathlib import Path
from pprintpp import pprint
import math
import pandas as pd
from collections import defaultdict
from datetime import date, timedelta, datetime

DEBUG_MODE = False

def debug_print(string):
  if DEBUG_MODE: print(string)

base_path = Path(__file__).parent
file_path = (base_path / "../data/raw_klines_data.m").resolve()
grouped_sets_path = (base_path / "../data/grouped_sets.m").resolve()
pocs_path = (base_path / "../data/pocs.m").resolve()
raw_data = open(file_path, "r")

klines_arr = raw_data.read().split('\n')
grouped_sets = sets_to_grouped_sets(klines_arr)
open(grouped_sets_path, "w").write("\n".join(grouped_sets))
first_set = grouped_sets[0]

first_ten_thousand = grouped_sets[:10000]
print(len(first_ten_thousand))

start_pointer = 0
end_pointer = 0
price_volume_dict = defaultdict(lambda: 0)

debug_print(f'size of grouped_sets {len(grouped_sets)}')

pd.set_option('display.float_format', '{:.2f}'.format)
df = pd.DataFrame()
start_csv_pointer = date(2019, 10, 1)
end_csv_pointer = start_csv_pointer

list_of_poc = []

# for index, set in enumerate(grouped_sets[0:4]): # to test.
for index, set in enumerate(first_ten_thousand):
  print(f'index {index}')
  
  start_timestamp = int(set.split(' ')[0])
  end_timestamp = start_timestamp + SET_INTERVAL

  start_day = date.fromtimestamp(start_timestamp)
  end_day = date.fromtimestamp(end_timestamp)

  debug_print(f"start_csv_pointer {start_csv_pointer}")
  debug_print(f"end_csv_pointer {end_csv_pointer}")

  debug_print(f"start_day {start_day}")
  debug_print(f"end_day {end_day}")

  while end_csv_pointer <= end_day + timedelta(days=1):
    debug_print(f"updating dataframe and moving end_csv_pointer.. {end_csv_pointer}")
    day_path = (base_path / f"../data/trades/{end_csv_pointer}").resolve()
    trades_for_day = pd.read_feather(day_path)
    df = pd.concat([df, trades_for_day[::-1]])
    end_csv_pointer += timedelta(days=1)
  

  while start_csv_pointer < start_day:
    debug_print(f"updating dataframe and moving start_csv_pointer.. {start_csv_pointer}")
    day_path = (base_path / f"../data/trades/{start_csv_pointer}").resolve()
    trades_for_day = pd.read_feather(day_path)
    num_rows_dropped = len(trades_for_day.index)
    df = df.iloc[num_rows_dropped: , :]
    start_csv_pointer += timedelta(days=1)
    start_pointer -= num_rows_dropped
    end_pointer -= num_rows_dropped

  df = df.reset_index(drop=True)

  debug_print("calculating poc.. ")

  # @ToDo here i can improve runtime by also keeping a heap.

  debug_print(f"{start_timestamp=}")
  debug_print(f"{start_pointer=}")
  df = df.rename(columns={'size': 'Size'})

  while df.timestamp[start_pointer] < start_timestamp: 
    price_volume_dict[df.price[start_pointer]] -= df.Size[start_pointer]
    start_pointer += 1
  debug_print(f"{start_pointer=}")
  debug_print(f"{df.timestamp[start_pointer]=}")

  debug_print(f"{end_timestamp=}")

  while end_pointer < len(df.index) and df.timestamp[end_pointer] <= end_timestamp :
    price_volume_dict[df.price[end_pointer]] += df.Size[end_pointer]
    end_pointer += 1
  debug_print(f"{end_pointer=}")
  debug_print(f"{df.timestamp[end_pointer]=}")

  df = df.rename(columns={'Size': 'size'})

  point_of_control = list(price_volume_dict.keys())[0]

  for key in price_volume_dict:
    if price_volume_dict[key] > price_volume_dict[point_of_control]:
      point_of_control = key

  list_of_poc.append(point_of_control)
  debug_print(f"current poc {list_of_poc}")

open(pocs_path, "w").write("\n".join(list(map(lambda x: str(x), list_of_poc))))
