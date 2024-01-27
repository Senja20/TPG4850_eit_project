"""
This module contains the class for dataset. 
"""
from torch import tensor, float32, long
from torch.utils.data import Dataset
from config import label_map


class HandLandmarksDataset(Dataset):
    """
    Data has to be processes before used in the neral network.
    This class is used for that processing.
    """

    def __init__(self, dataframe, label_column="Label"):
        self.data = dataframe
        self.label_column = label_column

        # Assuming the label column contains string labels, map them to integer values
        self.labels = tensor(
            self.data[self.label_column].map(label_map).values,
            dtype=long,
        )

        self.data = tensor(self.data.iloc[:, :-1].values, dtype=float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        landmarks = self.data[index].clone().detach()
        label = self.labels[index].clone().detach()
        return landmarks, label
