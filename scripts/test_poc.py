# for sibling imports
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.data_mutations import sets_to_grouped_sets
from utils.base_path import get_file_path
from utils.point_of_control import calc_point_of_control

raw_data = open(get_file_path("../data/raw_klines_data.m"), "r")

klines_arr = raw_data.read().split('\n')
grouped_sets = sets_to_grouped_sets(klines_arr)

print(calc_point_of_control(grouped_sets[8978]))
print(calc_point_of_control(grouped_sets[8979]))