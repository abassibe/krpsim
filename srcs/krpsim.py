import sys
import argparse
import time
from node import Node
from parser import parseFile
from printPath import printPath
from functionHeuristique import initialize, analyze
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


def createNewNode(processToAdd, parent, stock):
    countReward = 1
    for key, value in processToAdd.reward.items():
        if key in toOptimize:
            continue
        countReward += value
    parentScore = 0
    if parent != None:
        parentScore = parent.heuristique
    return Node(processToAdd, parent, parentScore + (processToAdd.delay / countReward), stock)


class coreThread(Thread):
    def __init__(self, node):
        Thread.__init__(self)
        self.node = node
        self.stock = node.stocks if node else initialStocks
        self.retValue = []

    def run(self):
        tmpOpenList = {}
        for func in processList:
            if func.canBeComputed(self.stock):
                if not self.node and func.name not in tmpOpenList:
                    newNode = createNewNode(func, None, self.stock)
                    newNode.cumulateDelay = func.delay
                    tmpOpenList[func.name] = newNode
                elif func.name not in tmpOpenList:
                    tmp = self.node.cumulateDelay
                    newNode = createNewNode(func, self.node, self.node.stocks)
                    newNode.cumulateDelay = tmp + func.delay
                    tmpOpenList[func.name] = newNode
        nodeToSave = None
        heurValue = 0
        for key, value in tmpOpenList.items():
            if value.heuristique > heurValue:
                heurValue = value.heuristique
            if value.parent and key == value.parent.funcToComput.name:
                nodeToSave = value
            self.retValue.append(value)
        if nodeToSave:
            nodeToSave.heuristique = heurValue + 10

    def join(self):
        Thread.join(self)
        return self.retValue


def sortCloseList():
    closeList.sort(key=lambda Node: Node.cumulateDelay)
    closeList.sort(key=lambda Node: Node.stocks['euro'], reverse=True)
    

# def searchPath():
#     global closeList
#     while startTime + args.delay > time.time():
#         runningThreads = []
#         if len(openList) <= 0:
#             break
#         for i in range(len(openList)):
#             if i > MAX_CPU_THREAD - 1:
#                 break
#             runningThreads.append(coreThread(openList[0]))
#             closeList.append(openList.pop(0))
#             runningThreads[i].start()
#         for thread in runningThreads:
#             newNodes = thread.join()
#             for node in newNodes:
#                 openList.append(node)
#         openList.sort(key=lambda Node: Node.heuristique)
#     sortCloseList()
#     printPath(closeList[0], initialStocks)
#     print('euro: ' + str(closeList[0].stocks['euro']))

def bestBranch(objectiveFunctions):
    toRet = None
    for func in objectiveFunctions.linkedFunction:
        if not toRet or toRet.score > func.score:
            toRet = func
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



def constructPath(bestFunction, path):
    queue = []
    queue.append(bestFunction)
    while len(queue) > 0:
        head = queue.pop(0)
        for cost in head.cost.keys():
            best = appendBestFunc(ressources[cost].linkedFunction)
            queue.append(best)
            path.append(best.name)
# construct path a besoin de link les parents pour ne pas boucler a l'infini
# rajouter la notion de nombre de fois oula fonction doit etre faite pour progresser dans l'arbre 
# genre si il faut faire 3x do_tarte_pomme dans l'idee il faudra faire 3 fois les fonctions qui sont link 
# garder un historique des resources ? pour arreter le parcours si on peut produire cash un truc ?
# faire construct path pour toutes les fonctions liees a l'objectif
# sur pomme il est possible que nous n'ayons pas les ressources necessaires pour faire vente boite
# du coup pick un autre chemin (le plus rentable) et regarder si le chemin le plus optimise est faisable


def searchPath(ressources):
    stackOfPath = []
    toSearch = bestBranch(ressources[toOptimize[0]])
    # stackOfPath.append(toSearch)
    constructPath(processList[15], stackOfPath)
    while startTime + args.delay > time.time():
        for func in processList:
            continue
 
    

parseFile(data, initialStocks, processList, toOptimize)
initialize(initialStocks, toOptimize, processList)
ressources = analyze()
start = coreThread(None)
start.start()
nodeList = start.join()
for node in nodeList:
    openList.append(node)
openList.sort(key=lambda Node: Node.heuristique)
searchPath(ressources)
