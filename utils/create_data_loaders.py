from torch.utils.data import DataLoader
from Classes.HandLandmarksDataset import HandLandmarksDataset


def create_data_loaders(train_set, val_set, batch_size):
    train_loader = DataLoader(
        HandLandmarksDataset(train_set), batch_size=batch_size, shuffle=True
    )
    val_loader = DataLoader(
        HandLandmarksDataset(val_set), batch_size=batch_size, shuffle=False
    )
    return train_loader, val_loader
