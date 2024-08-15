import numpy as np

class RecommendModel:
    def __init__(self):
        self.model = None
        print('Load recommend model: Done!')

    def predict(self, habit):
        a = np.arange(1, 6)
        np.random.shuffle(a)
        return a