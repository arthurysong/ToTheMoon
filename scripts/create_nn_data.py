# for sibling imports
import numpy as np

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config.params import KLINES_BEFORE, KLINES_AFTER, PERCENT_MOVEMENT_THRESHOLD
from utils.base_path import get_file_path
from utils.data_mutations import sets_to_grouped_sets
from pprintpp import pprint

raw_data = open(get_file_path("../data/raw_klines_data.m"), "r").read().split('\n')
raw_data_without_timestamps = list(map(lambda x: ' '.join(x.split(' ')[1:]), raw_data))
grouped_sets = sets_to_grouped_sets(raw_data_without_timestamps)

# print(grouped_sets[0])
# print(len(grouped_sets[0]))

def get_aggregations(set):
  # we only want to create aggregates from KLINES_BEFORE
  # lets create an array of all opens from all KLINES_BEFORE

  # first we need to create an array so we can index into each position
  set_array = set.split(" ")
  opens = []
  for i in range(KLINES_BEFORE):
    opens.append(float(set_array[i * 6]))
  np_opens = np.array(opens)

  # print(f"{np_opens.sum()=}")
  # print(f"{np_opens.mean()=}")
  # print(f"{np_opens.std()=}")
  # print(f"{np_opens.var()=}")
  # print(f"{np_opens.min()=}")
  # print(f"{np_opens.max()=}")
  # print(f"{np.median(np_opens)=}")
  # print(f"{np.percentile(np_opens, 25)=}")

  return [np_opens.sum(), np_opens.mean(), np_opens.std(), np_opens.var(), np_opens.min(), np_opens.max(), np.median(np_opens), np.percentile(np_opens, 25)]


# pocs = open(get_file_path("../data/pocs.m"), "r").read().split('\n')
# def get_poc(index):
#   return pocs[index]

def get_label(set):
  # this is getting the y value of the set.
  last_length = KLINES_AFTER * 6
  last_klines = set.split(" ")[-last_length:] 

  # get open from first and close from last 
  # get total price movement
  # and it should be > 1%
  first_open = float(last_klines[0])
  last_close = float(last_klines[-3])
  price_movement = (last_close - first_open) / first_open

  buy_sell_or_hold = None
  if price_movement > PERCENT_MOVEMENT_THRESHOLD:
    buy_sell_or_hold = "1" # buy
  elif price_movement < -PERCENT_MOVEMENT_THRESHOLD:
    buy_sell_or_hold = "0" # sell
  else:
    buy_sell_or_hold = "2" # hold

  # all_but_last_klines = set.split(" ")[0:-last_length]
  # all_but_last_klines.extend([str(first_open), buy_sell_or_hold])

  # return all_but_last_klines

  return buy_sell_or_hold;

def remove_klines_after(set):
  last_length = KLINES_AFTER * 6
  last_klines = set.split(" ")[-last_length:] 
  first_open = float(last_klines[0])
  all_except_last_klines = set.split(" ")[0:-last_length]
  # remove klines_after but keep the next open price 
  all_except_last_klines.extend([str(first_open)])
  return all_except_last_klines

first_set = grouped_sets[0]
# print(get_aggregations(grouped_sets[0]))
# print(get_poc(0))
# this should have a length of KLINES_BEFORE * 6 + 1
# print(KLINES_BEFORE * 6 + 1 == len(remove_klines_after(first_set)))
# print(remove_klines_after(first_set))
# print(len(remove_klines_after(first_set)))
# print(get_label(first_set))
print(len(first_set.split(" ")))
input()

first_labeled_set = f"{' '.join(remove_klines_after(first_set))} {get_poc(0)} {' '.join(list(map(lambda x: str(x), get_aggregations(first_set))))} {get_label(first_set)}"
# print(len(first_labeled_set.split(' ')) == KLINES_BEFORE * 6 + 1 + 8 + 1 + 1)

print(len(first_labeled_set.split(' ')))
input()
# print(first_labeled_set)


batch = grouped_sets[:10000]

def get_nn_data(set, index):
  return f"{' '.join(remove_klines_after(set))} {get_poc(index)} {' '.join(list(map(lambda x: str(x), get_aggregations(set))))} {get_label(set)}"

# "\n".join(list(map(get_nn_data)))
nn_data = []

for i, set in enumerate(batch):
  nn_data.append(get_nn_data(set, i))

# pprint(nn_data);
print(len(nn_data))
print(len(pocs))
# "\n".join(nn_data)

nn_file = open(get_file_path("../data/nn_data.m"), "w")
nn_file.write("\n".join(nn_data))
