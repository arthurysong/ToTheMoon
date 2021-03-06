from torch.utils.data import Dataset

class CustomDataset(Dataset):
  def __init__(self, data, labels, transform=None, target_transform=None):
    self.data = data
    self.labels = labels
    self.transform = transform
    self.target_transform = target_transform

  def __len__(self):
    return len(self.labels)

  def __getitem__(self, index):
    set = self.data[index, :]
    label = self.labels[index]
    return set, int(label)