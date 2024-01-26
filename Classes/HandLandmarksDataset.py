"""
This module contains the class for dataset. 
"""
import torch
from torch.utils.data import Dataset


class HandLandmarksDataset(Dataset):
    """
    Data has to be processes before used in the neral network.
    This class is used for that processing.
    """

    def __init__(self, dataframe, label_column="Label"):
        self.data = dataframe
        self.label_column = label_column

        # Assuming the label column contains string labels, map them to integer values
        self.labels = torch.tensor(
            self.data[self.label_column].map({"UP": 1.0, "DOWN": 0.0}).values,
            dtype=torch.long,
        )

        self.data = torch.tensor(self.data.iloc[:, :-1].values, dtype=torch.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        landmarks = self.data[idx].clone().detach()
        label = self.labels[idx].clone().detach()
        return landmarks, label
