import torch

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.base_path import get_file_path
from pprintpp import pprint
from torch import nn

data = open(get_file_path("../data/nn_data.m"), "r").read().split('\n')

def reformat_set(set):
  array = set.split(' ')
  int_array = [float(numeric_string) for numeric_string in array]
  return int_array

array_data = list(map(reformat_set, data))
x_data = torch.tensor(array_data)
print(x_data)

# now we need to create neural network
class NeuralNetwork(nn.Module):
  def __init__(self):
    super(NeuralNetwork, self).__init__()
    self.linear_relu_stack = nn.Sequential(
      nn.ReLu(),
      nn.Linear(4042, 300),
      nn.ReLu(),
      nn.Linear(300, 3),
      nn.Relu(),
    )

  def forward(self, x):
    logits = self.linear_relu_stack(x)
    return logits