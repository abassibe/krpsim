from function import Func
from copy import deepcopy
from ressource import Ressource

initialStocks = None
objective = None
processList = None
baseStock = {}
ressources = {}

def initialize(stock, toOptimize, function):
    global initialStocks
    global objective
    global processList
    global baseStock
    initialStocks = stock
    objective = toOptimize
    processList = function
    for key, value in initialStocks.items():
        if value > 0:
            baseStock[key] = value

def getAssociatedCostFunction(cost):
    targetedFunc = []
    for func in processList:
        if cost in func.reward:
            targetedFunc.append(func)
    return targetedFunc

def clearStock(operateStock):
    for key in baseStock:
        operateStock[key] = 0

def associateRessource(ressource):
    for key, value in initialStocks.items():
        ressource[key] = Ressource(key, value)

def getlinkedFunctions():
    for key, value in ressources.items():
        for func in processList:
            if key in func.reward:
                value.addLink(func)

def computScore(tmpStock, linked):
    totalCost = 0
    for costKey, costValue in linked.cost.items():
        totalCost += tmpStock[costKey] * costValue
    totalCost /= len(linked.cost)
    try:
        for keyReward, rewardValue in linked.reward.items():
            total = totalCost / rewardValue
            if tmpStock[keyReward] == 0 or keyReward in objective:
                total = totalCost / rewardValue
                tmpStock[keyReward] = total
            else:
                total = tmpStock[keyReward]
            if keyReward in linked.cost and rewardValue < linked.cost[keyReward]:
                total = 999999999
            linked.rewardsScore[keyReward] = total
            linked.rewardsScoreWithDelay[keyReward] = total * linked.delay
            linked.calculateScore()
    except:
        exit("Wrong rewards value.")

def isScored():
    for process in processList:
        if process.score == 0:
            return False
    return True

def canBeScored(func, tmpStock):
    for cost in func.cost.keys():
        if tmpStock[cost] == 0:
            return False
    return True

def isProcessUseless():
    for index, process in enumerate(processList):
        if process.reward == process.cost:
            processList.pop(index)

def calculateHeuristic():
    tmpStock = deepcopy(initialStocks)
    isProcessUseless()
    for key, value in tmpStock.items():
        if value > 0:
            tmpStock[key] = 1
    
    while not isScored():
        for func in processList:
            if canBeScored(func, tmpStock):
                computScore(tmpStock, func)


def analyze():
    global ressources
    associateRessource(ressources)
    objectiveFunction = {}
    operateStock = deepcopy(initialStocks)
    clearStock(operateStock)
    for opti in objective:
        for func in processList:
            if opti in func.reward:
                objectiveFunction[func] = deepcopy(operateStock)
    getlinkedFunctions()
    calculateHeuristic()
    return ressources
