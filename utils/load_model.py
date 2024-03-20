"""
Load the existing model and device
"""

from os import getenv

from dotenv import load_dotenv

from Classes.GestureClassifier import GestureClassifier


def load_model(device) -> GestureClassifier:
    """
    desc: Method used for loading the model.
    :param device: The device on which the model will be loaded.
    :return: The loaded model.
    """

    load_dotenv()

    # loaded_model = load("gesture_model.pth")

    loaded_model = GestureClassifier.from_pretrained(getenv("REPO_ID"))

    loaded_model.eval()
    return loaded_model.to(device)
