"""
Load the existing model and device
"""

from torch import load


def load_model(device):
    """
    desc: Method used for loading the model.
    :param device: The device on which the model will be loaded.
    :return: The loaded model.
    """

    loaded_model = load("gesture_model.pth")
    loaded_model.eval()
    return loaded_model.to(device)
