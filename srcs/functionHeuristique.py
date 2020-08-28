from function import Func
from copy import deepcopy
from ressource import Ressource

initialStocks = None
objective = None
processList = None
baseStock = {}

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

def calculateHeuristic(functions, objectiveQuantity):
    costTotal = 0
    bestScore = 999999999
    toReturn = None
    for func in functions:
        for value in func.cost.values():
            costTotal += value
            if (costTotal / objectiveQuantity) * func.delay < bestScore:
                bestScore = (costTotal / objectiveQuantity) * func.delay
                toReturn = func
    return toReturn

def searchPath(target, stock):
    for functions in target:
        targetedFunc = []
        for costs, value in functions.cost.items():
            if costs in baseStock:
                return
            targetedFunc = getAssociatedCostFunction(costs)
            if len(targetedFunc) > 1:
                targetedFunc = [calculateHeuristic(targetedFunc, value)]
            print(targetedFunc[0].name)
            stock[costs] += value
            searchPath(targetedFunc, stock)

def clearStock(operateStock):
    for key in baseStock:
        operateStock[key] = 0

def associateRessource(ressource):
    for key, value in initialStocks.items():
        ressource[key] = Ressource(key, value)

def analyze():
    ressources = {}
    associateRessource(ressources)
    objectiveFunction = {}
    operateStock = deepcopy(initialStocks)
    clearStock(operateStock)
    for opti in objective:
        for func in processList:
            if opti in func.reward:
                objectiveFunction[func] = deepcopy(operateStock)
                ressources[opti].addLink(func)
    for key, value in objectiveFunction.items():
        searchPath([key], value)
        # print()

# pour chaque fonctions de objectiveFunction
# regarder les couts 
# pour chaque couts regarder les fonctions qui les produisent
