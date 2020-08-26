import copy

class Node:
    def __init__(self, funcToComput, parent, score, stock):
        self.funcToComput = funcToComput
        self.parent = parent
        self.heuristique = score
        self.stocksBeforeCompute = copy.deepcopy(stock)
        self.stocks = self.funcToComput.compute(copy.deepcopy(stock))
        self.cumulateDelay = 0
