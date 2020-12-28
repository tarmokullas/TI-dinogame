import numpy as np


def sigmoid(z):
    return 0.5 * (1 + np.tanh(0.5 * z))


class Genome:
    def __init__(self, L1=None, L2=None):
        self.input_size = 5
        self.hidden_size = 12
        self.output_size = 2
        self.L1 = np.random.randn(self.input_size, self.hidden_size) if L1 is None else L1
        self.L2 = np.random.randn(self.hidden_size, self.output_size) if L2 is None else L2
        self.score = 0

    def predict(self, input):
        z = input.dot(self.L1)
        a2 = sigmoid(z)
        z2 = a2.dot(self.L2)
        result = sigmoid(z2)
        return result

    def getData(self):
        return [self.L1.tolist(), self.L2.tolist()]
