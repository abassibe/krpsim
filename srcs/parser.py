import re
from function import Func

isTimed = False

def isStock(line):
    pattern = re.compile(r"^(\w+):\d+")
    return re.match(pattern, line)

def isProcess(line):
    if line.startswith("optimize"):
        return None
    pattern = re.compile(r"^(\w+):\(")
    return re.match(pattern, line)


def splitStock(stock):
    stock = stock.split(":")
    if len(stock) > 2:
        return 
    return stock[0], stock[1]

def getStock(line, stocks, processList):
    stockName, quantity = splitStock(line)
    if stockName and quantity:
        stocks[stockName] = int(quantity)

def splitProcess(line):
    name = line[:line.find(":")]
    delay = line[line.rfind(":") + 1:]
    
    costs = line[line.find("(") + 1:line.find(")")]
    rewards = line[line.rfind("(") + 1:line.rfind(")")]

    costsDict = {}
    rewardsDict = {}
    
    realCosts = costs.split(";")
    realRewards = rewards.split(";")
    
    for cost in realCosts:
        costName, quantity = tuple(cost.split(":"))
        costsDict[costName] = int(quantity)
    
    for reward in realRewards:
        rewardName, quantity = tuple(reward.split(":"))
        rewardsDict[rewardName] = int(quantity)
    
    return name, costsDict, rewardsDict, delay

def getProcess(line, initialStocks, processList):
    processName, costs, rewards, delay = splitProcess(line)
    for key in costs.keys():
        if key not in initialStocks:
            initialStocks[key] = 0
    for key in rewards.keys():
        if key not in initialStocks:
            initialStocks[key] = 0
    processList.append(Func(processName, costs, rewards, delay))


def isObjective(line):
    return line.startswith("optimize")

def getObjective(line, toOptimize):
    global isTimed
    tmpToOptimize = line[line.find("(") + 1:line.find(")")]
    tmpToOptimize = tmpToOptimize.split(";")
    for elem in tmpToOptimize:
        if elem == 'time':
            isTimed = True
            continue
        toOptimize.append(elem)

def parseFile(data, initialStocks, processList, toOptimize):
    for line in data:
        if line[0] == "#":
            continue
        if isStock(line):
            getStock(line, initialStocks, processList)
        elif isProcess(line):
            getProcess(line, initialStocks, processList)
        elif isObjective(line):
            getObjective(line, toOptimize)

def isTime():
    return isTimed