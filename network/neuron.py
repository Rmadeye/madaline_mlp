class SingleNeuron:
    def __init__(self, weights: np.array, labels: list):
        self.labels = labels
        self.weights = weights

    def forward(self, x):
        return x @ self.weights