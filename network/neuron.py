import numpy as np

class SingleNeuron:
    def __init__(self, weights: np.array, labels: list):
        self.labels = labels
        self.weights = weights

    def forward(self, x):
        # breakpoint()
        return x @ self.weights.T