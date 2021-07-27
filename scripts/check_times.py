#! /usr/bin/python3

# for sibling imports
# script that checks all klines are 900 seconds (15 min apart)
# no repeats, no gap from start to end

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.plot import plot_klines
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "../data/raw_klines_data.m").resolve()
file = open(file_path, "r")

data_str = file.read()
klines = data_str.split('\n')
klines = list(map(lambda a: int(a.split(' ')[0]), klines))
print(klines)

def check_times(times): 
  i = 0
  while i < len(times) - 1:
    print(f'current {times[i]}')
    if times[i] != times[i+1] - 900:
      print(times[i])
      return False
    i += 1
  return True

print(f'correctly fetched all 900 second intervals from start to end {check_times(klines)}')