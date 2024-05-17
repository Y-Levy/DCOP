import numpy as np
import random


class UniConstraints:
    def __init__(self, domainSize, low=0, high=100):
        self.domainSize = domainSize
        self.low = low
        self.high = high

    def create_constraint(self):
        matrix = []
        for row in range(self.domainSize):
            row = []
            for assignment in range(self.domainSize):
                uti = random.uniform(self.low, self.high)
                utility = round(uti, 2)
                row.append(utility)
            matrix.append(row)
        return matrix
