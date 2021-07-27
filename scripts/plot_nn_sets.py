#! /usr/bin/python3

from pathlib import Path

# for sibling imports
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.data_mutations import sets_to_grouped_sets
from utils.plot import plot_one_set

base_path = Path(__file__).parent
file_path = (base_path / "../data/raw_klines_data.m").resolve()
raw_data = open(file_path, "r")

klines_arr = raw_data.read().split('\n')
sets_of_51 = sets_to_grouped_sets(klines_arr)
for num, set in enumerate(sets_of_51, start=1):
  print("plotting line ", num)
  plot_one_set(set)