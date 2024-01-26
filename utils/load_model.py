from torch import load


def load_model(device):
    """
    desc: Method used for loading the model.
    :return: The loaded model.
    """

    loaded_model = load("gesture_model.pth")
    loaded_model.eval()  # Set the model to evaluation mode
    return loaded_model.to(device)
