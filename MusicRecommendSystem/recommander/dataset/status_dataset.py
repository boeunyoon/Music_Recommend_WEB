import torch
from torch.utils.data import Dataset, DataLoader

class StatusDataset(Dataset):
    def __init__(self, stat_tensor):
        self.stat_tensor = stat_tensor

    def __len__(self):
        return self.stat_tensor.shape[0]

    def __getitem__(self, index):
        return self.stat_tensor[index]