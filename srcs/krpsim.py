import sys
import argparse
import time
from node import Node
from parser import parseFile
from printPath import printPath
from functionHeuristique import initialize, analyze
from math import ceil
from threading import Thread
import multiprocessing 

startTime = time.time()
parser = argparse.ArgumentParser(description='Krp', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-p", "--path", required=True, type=str, help="Path to the process to optimize.")
parser.add_argument("-d", "--delay", type=int, required=True, help="delay")

args = parser.parse_args()

if args.delay < 0:
    exit("Must be positive.")

data = []
openList = []
closeList = []

processList = []
initialStocks = {}
toOptimize = []

MAX_CPU_THREAD = multiprocessing.cpu_count()

try:
    with open(args.path) as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.strip())
except:
    exit("Cannot open file.")


def bestBranch(objectiveFunctions, toOptimize):
    toRet = objectiveFunctions.linkedFunction[:]
    toRet.sort(key=lambda Func: Func.rewardsScore[toOptimize])
    return toRet

def requiredRessources(func):
    for costKey, costValue in func.cost.items():
        if initialStocks[costKey] < costValue:
            return False
    return True

def appendBestFunc(linkedFunction):
    toRet = None
    for func in linkedFunction:
        if not toRet or toRet.score > func.score:
            toRet = func
    return toRet


def searchPath(ressources, toProduce, stackOfPath, amountToProduce):
    if toProduce == toOptimize[0] and amountToProduce > 0:
        return
    toSearch = bestBranch(ressources[toProduce], toProduce)
    if len(toSearch) < 1:
        return
    toExec = toSearch[0]
    execCount = ceil((amountToProduce - initialStocks[toProduce]) / toExec.reward[toProduce])
    if execCount < 1:
        execCount = 1
    if not toExec.canBeComputedNTimes(initialStocks, execCount):
        for ressourcesName, ressourcesNeeded in toExec.cost.items():
            if ressourcesName in toExec.reward and toExec.reward[ressourcesName] == ressourcesNeeded:
                continue
            if not initialStocks[ressourcesName] >= ressourcesNeeded * execCount:
                searchPath(ressources, ressourcesName, stackOfPath, ressourcesNeeded * execCount)
    if toExec.canBeComputedNTimes(initialStocks, execCount):
        tmp = toSearch.pop(0)
        for i in range(execCount):
            toExec.compute(initialStocks)
            # print(tmp.name)
            stackOfPath.append(tmp)
 

parseFile(data, initialStocks, processList, toOptimize)
initialize(initialStocks, toOptimize, processList)
ressources = analyze()
stackOfPath = []
while startTime + args.delay > time.time():
    searchPath(ressources, toOptimize[0], stackOfPath, -1)
    if len(stackOfPath) == 0:
        break
    for path in stackOfPath:
        print(path.name)
    stackOfPath.clear()
    # exit()
print(initialStocks)
