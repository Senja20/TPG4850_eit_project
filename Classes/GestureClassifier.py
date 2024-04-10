"""
This module contains the class used for the neural network. 
The class initializes the NN and performs forward propagation. 
The class was created to be imported by other modules.
"""

from os import getenv

from dotenv import load_dotenv
from huggingface_hub import PyTorchModelHubMixin
from torch.nn import Linear, Module, ReLU, Softmax


class GestureClassifier(Module, PyTorchModelHubMixin):
    """
    The class contains the NN used to classify gestures based on provided data.
    """

    load_dotenv()

    def __init__(
        self,
        input_layer_size=int(getenv("NUMBER_LANDMARKS"))
        * int(getenv("NUMBER_OF_CHANNELS")),
        hidden_layer_size=64,
        output_layer_size=int(getenv("OUTPUT_LAYER")),
    ) -> None:
        super().__init__()
        self.fc1 = Linear(input_layer_size, hidden_layer_size)
        self.relu = ReLU()
        self.fc2 = Linear(hidden_layer_size, output_layer_size)
        self.softmax = Softmax()

    def forward(self, x):
        """
        desc: Method used for perform forward propagation.

        Parameters:
        ----------
        x : tensor
            The input data which is used to make predictions.

        Returns
        -------
        int
            Score on which is the most likely class to be detected.
        """
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x
