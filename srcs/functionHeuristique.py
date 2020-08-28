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

def searchPath(target):
    for functions in target:
        targetedFunc = []
        for costs, value in functions.cost.items():
            if costs in baseStock:
                return
            targetedFunc = getAssociatedCostFunction(costs)
            for func in targetedFunc:
                ressources[costs].addLink(func)
            searchPath(targetedFunc)

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

def computScore(tmpStock, key, linked):
    total = 0
    for func in processList:
        for key, rewardValue in func.reward.items():
            print()
            for key, costValue in func.cost.items():
                total += rewardValue / costValue
    return 0

def calculateHeuristic():
    tmpProcessList = deepcopy(processList)
    tmpStock = deepcopy(initialStocks)
    for key, value in tmpStock.items():
        if value > 0:
            tmpStock[key] = 1
    while len(tmpStock) > 0:
        for key, value in tmpStock.items():
            if value <= 0:
                continue
            for linked in tmpProcessList:
                if key in linked.cost and key not in linked.reward:
                    linked.rewardsScore = computScore(tmpStock, key, linked)

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
    for key in objectiveFunction.keys():
        searchPath([key])
        # print()
