from torch import nn

class NeuralNetwork(nn.Module):
  def __init__(self):
    super(NeuralNetwork, self).__init__()
    self.linear_relu_stack = nn.Sequential(
      # nn.ReLU(),
      nn.Linear(4042, 512),
      nn.BatchNorm1d(512),
      nn.ReLU(),

      nn.Linear(512, 128),
      nn.BatchNorm1d(128),
      nn.ReLU(),
      nn.Dropout(p=0.2),

      nn.Linear(128, 3),
    )

  def forward(self, x):
    logits = self.linear_relu_stack(x)
    return logits