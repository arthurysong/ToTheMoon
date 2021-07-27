# take a start timestamp
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config.params import SET_INTERVAL
from utils.base_path import get_file_path
from pathlib import Path
import pandas as pd
from collections import defaultdict
from datetime import date, timedelta

base_path = Path(__file__).parent
file_path = (base_path / "../data/trades").resolve()

def calc_point_of_control(set):

  start_timestamp = int(set.split(' ')[0])
  end_timestamp = start_timestamp + SET_INTERVAL

  day = date.fromtimestamp(start_timestamp)
  df = pd.DataFrame();

  for i in range(9):
    day += timedelta(days=1)
    print(day);
    trades_for_day = pd.read_feather(get_file_path(f"../data/trades/{day}"))
    df = pd.concat([df, trades_for_day[::-1]])

  df = df.reset_index(drop=True)
  price_volume_dict = defaultdict(lambda: 0)
  start_timestamp = int(set.split(' ')[0])
  print(start_timestamp)
  print(df)
  mask = (df['timestamp'] > start_timestamp) & (df['timestamp'] <= end_timestamp)
  trades_made_for_set = df.loc[mask]

  print(f"{start_timestamp=}")
  print(f"{end_timestamp=}")
  for index, row in trades_made_for_set.iterrows():
    price_volume_dict[row['price']] += row['size']

  # print(dict(price_volume_dict))
  point_of_control = list(price_volume_dict.keys())[0]

  for key in price_volume_dict:
    if price_volume_dict[key] > price_volume_dict[point_of_control]:
      point_of_control = key

  return point_of_control

