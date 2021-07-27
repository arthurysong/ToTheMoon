#! /usr/bin/python3

# for sibling imports
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
plot_klines(klines)