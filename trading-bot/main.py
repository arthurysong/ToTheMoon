# websockets subscribe to trades and klines
# once we get 7 days worth of trades and klines
# we can start capturing a set of features
# and use our nn to predict ? 

# so each time we want to test we need to wait 7 days.. that's pretty shit.
# i need to train nn to be able to accept a smaller time frame?
# so even if 4042 features we can just feed like 100
import os
import asyncio
# import websockets
# print(os.environ['BYBIT_API_KEY'])
BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
BYBIT_SECRET = os.environ['BYBIT_SECRET']

async def connect():
  uri = "wss://stream.bybit.com/realtime"
  # expires = time.

import torch

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from utils.base_path import get_file_path
# from pprintpp import pprint
# from torch import nn
# from torch.utils.data import DataLoader, Dataset
# from nn import NeuralNetwork
# from dataset import CustomDataset

data = open(get_file_path("../data/nn_data.m"), "r").read().split('\n')
print(len(data))