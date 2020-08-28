from copy import deepcopy

cycle = 0

def constructOutput(toExec):
    global cycle
    output = ""
    tmpCycle = 0

    for node in toExec:
        output += node.funcToComput.name
        output += ':'
        if node.funcToComput.delay > tmpCycle:
            tmpCycle = node.funcToComput.delay
    output = output[:-1]
    cycle += tmpCycle
    return f"{cycle}:{output}"
    

def printPath(path, initialStocks):
    actualStocks = deepcopy(initialStocks)
    toPrint = []
    toExec = []
    tmp = path
    i = 0

    while tmp.parent:
        toPrint.append(tmp)
        tmp = tmp.parent

    toPrint.append(tmp)
    toPrint.reverse()
    
    while i < len(toPrint):
        if toPrint[i].funcToComput.canBeComputed(actualStocks):
            save = toPrint.pop(i)
            for key, value in save.funcToComput.cost.items():
                actualStocks[key] -= value
            toExec.append(save)
            i -= 1
        if len(toExec) > 0 and i + 1 == len(toPrint):    
            for node in toExec:
                for key, value in node.funcToComput.reward.items():
                    actualStocks[key] += value
            print(constructOutput(toExec))
            toExec.clear()
            i = 0
        else:
            i += 1
