"""
This module contains the class used for the neural network. 
The class initializes the NN and performs forward propagation. 
The class was created to be imported by other modules.
"""

import torch.nn as nn


class GestureClassifier(nn.Module):

    """
    The class contains the NN used to classify gestures based on provided data.
    """

    def __init__(self, input_layer_size, hidden_layer_size, output_layer_size):
        super(GestureClassifier, self).__init__()
        self.fc1 = nn.Linear(input_layer_size, hidden_layer_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_layer_size, output_layer_size)

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
        return x
