from copy import deepcopy

class Func:
    def __init__(self, name, cost=None, reward=None, delay=1):
        self.cost = cost
        self.reward = reward
        self.costByRewards = deepcopy(self.reward)
        self.delay = int(delay)
        self.name = name
        self.score = self.calculateScore()
        self.rewardOf = [] # Liste des functions qui ont besoin de ce que cette fonction produit
        self.costOf = [] # Liste des functions qui fournissent ce dont cette fonction a besoin

    def calculateScore(self):
        total = 0
        for cost in self.cost.values():
            total += cost * self.delay
        for reward in self.reward.values():
            total -= reward * self.delay
        return total

    def canBeComputed(self, items):
        for key, val in self.cost.items():
            if not items[key] >= val:
                return False
        return True

    def compute(self, stocks):
        for key, value in self.cost.items():
            stocks[key] -= value
        for key, value in self.reward.items():
            stocks[key] += value
        return stocks