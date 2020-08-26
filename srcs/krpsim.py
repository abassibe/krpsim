import sys
import argparse
import time
from node import Node
from parser import parseFile
from printPath import printPath

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


try:
    with open(args.path) as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.strip())
except:
    exit("Cannot open file.")


def createNewNode(processToAdd, parent, stock):
    countReward = 0
    for key, value in processToAdd.reward.items():
        if key in toOptimize:
            continue
        countReward += value
    parentScore = 0
    if parent != None:
        parentScore = parent.heuristique
    return Node(processToAdd, parent, parentScore + (processToAdd.delay / countReward), stock)


def searchValideFunction(stock, firstCall):
    tmpOpenList = {}
    for func in processList:
        if func.canBeComputed(stock):
            if firstCall and func.name not in tmpOpenList:
                newNode = createNewNode(func, None, stock)
                newNode.cumulateDelay = func.delay
                tmpOpenList[func.name] = newNode
            elif func.name not in tmpOpenList:
                tmp = openList[0].cumulateDelay
                newNode = createNewNode(func, openList[0], openList[0].stocks)
                newNode.cumulateDelay = tmp + func.delay
                tmpOpenList[func.name] = newNode
    nodeToSave = None
    heurValue = 0
    for key, value in tmpOpenList.items():
        if value.heuristique > heurValue:
            heurValue = value.heuristique
        if value.parent and key == value.parent.funcToComput.name:
            nodeToSave = value
        openList.append(value)
    if nodeToSave:
        nodeToSave.heuristique = heurValue + 10
    if not firstCall:
        closeList.append(openList.pop(0))
    openList.sort(key=lambda Node: Node.heuristique)
    print(end='')


def sortCloseList():
    closeList.sort(key=lambda Node: Node.cumulateDelay)
    closeList.sort(key=lambda Node: Node.stocks['euro'], reverse=True)
    

def searchPath():
    global closeList
    while startTime + args.delay > time.time():
        if len(openList) <= 0:
            break
        searchValideFunction(openList[0].stocks, False)
    sortCloseList()
    printPath(closeList[0], initialStocks)
    print('euro: ' + str(closeList[0].stocks['euro']))


parseFile(data, initialStocks, processList)
searchValideFunction(initialStocks, True)
openList.sort(key=lambda Node: Node.heuristique)
searchPath()
