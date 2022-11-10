import random as rnd
import numpy as np

class Agent:
    def __init__(self, index, strategy):
        self.index = index
        self.strategy = strategy
        self.reproductive = False
        self.points = 0

    def judge_reproductive(self, avg):
        if self.points >= avg:
            self.reproductive = True






