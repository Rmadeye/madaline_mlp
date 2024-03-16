import numpy as np


class SingleNeuron:
    """
    Represents a single neuron in a neural network.

    Args:
        weights (np.array): The weights of the neuron.
        labels (list): The labels associated with the neuron.

    Attributes:
        weights (np.array): The weights of the neuron.
        labels (list): The labels associated with the neuron.
    """

    def __init__(self, weights: np.array, labels: list):
        self.labels = labels
        self.weights = weights

    def forward(self, x):
        """
        Performs the forward pass of the neuron.

        Args:
            x: The input to the neuron.

        Returns:
            The output of the neuron.
        """
        return x @ self.weights.T
