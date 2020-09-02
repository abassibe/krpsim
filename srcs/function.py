from copy import deepcopy

class Func:
    def __init__(self, name, cost=None, reward=None, delay=1):
        self.cost = cost
        self.reward = reward
        self.rewardsScore = deepcopy(self.reward)
        self.rewardsScoreWithDelay = deepcopy(self.reward)
        self.delay = int(delay)
        self.name = name
        self.score = 0
        self.rewardOf = [] # Liste des functions qui ont besoin de ce que cette fonction produit
        self.costOf = [] # Liste des functions qui fournissent ce dont cette fonction a besoin

    def calculateScore(self):
        for reward in self.rewardsScoreWithDelay.values():
            self.score += reward
        self.score /= len(self.rewardsScoreWithDelay)


    def canBeComputed(self, items):
        for key, val in self.cost.items():
            if not items[key] >= val:
                return False
        return True

    def canBeComputedNTimes(self, items, quantity):
        tmpStock = deepcopy(items)
        for key, value in self.cost.items():
            tmpStock[key] -= value * quantity
        for key, value in self.reward.items():
            tmpStock[key] += value * quantity
        for val in tmpStock.values():
            if val < 0:
                return False
        return True

    def compute(self, stocks):
        for key, value in self.cost.items():
            stocks[key] -= value
        for key, value in self.reward.items():
            stocks[key] += value
        return stocks
