"""
Create data loaders function.
"""

from torch.utils.data import DataLoader

from Classes.HandLandmarksDataset import HandLandmarksDataset


def create_data_loaders(train_set, val_set, batch_size):
    """
    desc: Function used to create data loaders.
    :param train_set: The training set.
    :param val_set: The validation set.
    :param batch_size: The batch size.
    :return: The training and validation data loaders.
    """
    train_loader = DataLoader(
        HandLandmarksDataset(train_set), batch_size=batch_size, shuffle=True
    )
    val_loader = DataLoader(
        HandLandmarksDataset(val_set), batch_size=batch_size, shuffle=False
    )
    return train_loader, val_loader
