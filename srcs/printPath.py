from copy import deepcopy

cycle = 0

def constructOutput(toExec):
    global cycle
    output = ""
    tmpCycle = 0

    if len(toExec) < 1:
        return ''
    for node in toExec:
        output += node.name
        output += ':'
        if node.delay > tmpCycle:
            tmpCycle = node.delay
    output = output[:-1]
    cycle += tmpCycle
    return f"{cycle}:{output}\n"
    

def printPath(stackOfPath, stocks):
    toComput = []
    listOfIndex = []
    toPrint = ""
    while len(stackOfPath) > 0:
        for i, path in enumerate(stackOfPath):
            if path.canBeComputed(stocks):
                path.computeCost(stocks)
                toComput.append(path)
                listOfIndex.append(i)
        toPrint += constructOutput(toComput)
        for pathToComput in toComput:
            pathToComput.computeReward(stocks)
            stackOfPath.pop(listOfIndex.pop())
        toComput.clear()
    print(toPrint, end='')
