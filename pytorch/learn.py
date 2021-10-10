import torch

# ===== sibling imports ======
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# ===== sibling imports ======

from utils.base_path import get_file_path
from pprintpp import pprint
from torch import nn
from torch.utils.data import DataLoader, Dataset
from nn import NeuralNetwork
from dataset import CustomDataset

data = open(get_file_path("../data/nn_data.m"), "r").read().split('\n')

def reformat_set(set):
  array = set.split(' ')
  int_array = [float(numeric_string) for numeric_string in array]
  return int_array

array_data = list(map(reformat_set, data))
x_data = torch.tensor(array_data)

training_set_size = int(len(array_data) * .8)
last_index_of_training_set = training_set_size - 1
training_data = x_data[0:training_set_size, 0:4042]
training_label = x_data[0:training_set_size, 4042]
test_data = x_data[training_set_size:, 0:4042]
test_label = x_data[training_set_size:, 4042]


training_set = CustomDataset(training_data, training_label)
test_set = CustomDataset(test_data, test_label)

train_dataloader = DataLoader(training_set, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_set, batch_size=64, shuffle=True)

train_features, train_labels = next(iter(train_dataloader))

model = NeuralNetwork()

learning_rate = 1e-5
batch_size = 64
epochs = 300
loss_fn = nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

def train_loop(dataloader, model, loss_fn, optimizer):
  size = len(dataloader.dataset)
  for batch, (X, y) in enumerate(dataloader):
    # Compute prediction and loss
    pred = model(X)
    loss = loss_fn(pred, y)

    # Backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if batch % 100 == 0:
        loss, current = loss.item(), batch * len(X)
        print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test_loop(dataloader, model, loss_fn):
  size = len(dataloader.dataset)
  num_batches = len(dataloader)
  test_loss, correct = 0, 0

  preds = []
  with torch.no_grad():
      for X, y in dataloader:
          pred = model(X)
          preds.append(pred)
          test_loss += loss_fn(pred, y).item()
          correct += (pred.argmax(1) == y).type(torch.float).sum().item()

  test_loss /= num_batches
  correct /= size
  print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

for t in range(epochs):
  print(f"Epoch {t+1}\n-------------------------------")
  train_loop(train_dataloader, model, loss_fn, optimizer)
  test_loop(test_dataloader, model, loss_fn)

torch.save(model.state_dict(), 'nn_weights')
print("Done!")