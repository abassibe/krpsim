import argparse
from copy import deepcopy
from time import time
from math import ceil
from parser import parseFile, isTime
from printPath import printPath
from functionHeuristique import initialize, analyze

startTime = time()
parser = argparse.ArgumentParser(description='Krpsim', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-p", "--path", required=True, type=str, help="Path to the process to optimize.")
parser.add_argument("-d", "--delay", required=True, type=int, help="Delay")

args = parser.parse_args()

if args.delay < 0:
    exit("Delay must be positive.")

data = []

openList = []
closeList = []
processList = []
initialStocks = {}
toOptimize = []

try:
    with open(args.path) as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.strip())
except:
    exit("Process file cannot be opened.")


def bestBranch(objectiveFunctions, toOptimize):
    toRet = objectiveFunctions.linkedFunction[:]
    toRet.sort(key=lambda Func: Func.rewardsScore[toOptimize])
    return toRet


def requiredRessources(func):
    for costKey, costValue in func.cost.items():
        if updatedStock[costKey] < costValue:
            return False
    return True


def appendBestFunc(linkedFunction):
    toRet = None
    for func in linkedFunction:
        if not toRet or toRet.score > func.score:
            toRet = func
    return toRet


def isClosedPath(closeList, toSearch):
    for openPath in toSearch:
        if openPath not in closeList:
            return openPath
    return None


def isStockLeft():
    for stockKey, stockValue in updatedStock.items():
        if stockKey == toOptimize[0]:
            continue
        if stockValue > 0:
            return True
    return False


def searchPath(ressources, toProduce, stackOfPath, amountToProduce):
    if toProduce == toOptimize[0] and amountToProduce > 0:
        return
    toSearch = bestBranch(ressources[toProduce], toProduce)
    if len(toSearch) < 1:
        return
    toExec = None
    if len(closeList) > 0:
        toExec = isClosedPath(closeList, toSearch)
    else:
        toExec = toSearch[0]
    if not toExec:
        return False
    closeList.append(toExec)
    execCount = ceil((amountToProduce - updatedStock[toProduce]) / toExec.reward[toProduce])
    if execCount < 1:
        execCount = 1
    if not toExec.canBeComputedNTimes(updatedStock, execCount):
        for ressourcesName, ressourcesNeeded in toExec.cost.items():
            if ressourcesName in toExec.reward and toExec.reward[ressourcesName] == ressourcesNeeded:
                continue
            if not updatedStock[ressourcesName] >= ressourcesNeeded * execCount:
                if not searchPath(ressources, ressourcesName, stackOfPath, ressourcesNeeded * execCount):
                    return False
                break
        if isTime() and isStockLeft():
            searchPath(ressources, ressourcesName, stackOfPath, ressourcesNeeded * execCount)
    else:
        for i in range(execCount):
            toExec.compute(updatedStock)
            stackOfPath.append(toExec)
        toSearch.remove(toExec)
    return True


closeList = []
parseFile(data, initialStocks, processList, toOptimize)
initialize(initialStocks, toOptimize, processList)
updatedStock = deepcopy(initialStocks)
ressources = analyze()
stackOfPath = []
while startTime + args.delay > time():
    if not searchPath(ressources, toOptimize[0], stackOfPath, -1):
        printPath(stackOfPath, initialStocks)
        break
    if len(stackOfPath) == 0:
        break
    if len(stackOfPath) > 1000:
        printPath(stackOfPath, initialStocks)
        stackOfPath.clear()
    closeList.clear()
if len(stackOfPath) > 0:
    printPath(stackOfPath, initialStocks)
print('\nState of stock after ' + str(args.delay) + ' secondes')
for stockKey, stockValue in updatedStock.items():
    print(stockKey + ': ' + f'{stockValue:,}')
