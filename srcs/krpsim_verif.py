import argparse
from parser import parseFile, isTime

parser = argparse.ArgumentParser(description='Krpsim_verif', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-p", "--path", required=True, type=str, help="Path to the process to optimize.")
parser.add_argument("-c", "--check", required=True, type=str, help="Output to be checked")

args = parser.parse_args()

data = []

output = []
initialStocks = {}
processList = []
toOptimize = []

try:
    with open(args.path) as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.strip())
except:
    exit("Process file cannot be opened.")

try:
    with open(args.check) as f:
        lines = f.readlines()
        for line in lines:
            output.append(line.strip())
except:
    exit("Output file cannot be opened.")


def funcDictionaryBuild():
    ret = {}
    for func in processList:
        ret[func.name] = func
    return ret


def parseLine(line, functions, localCycle):
    splitedLine = line.split(':')
    tmpCycle = 0
    currentFunc = None
    try:
        actualFileCycle = int(splitedLine.pop(0))
    except:
        print("Error: output file wrongly formated.")
        exit()
    if actualFileCycle == 730:
        print()
    for func in splitedLine:
        try:
            currentFunc = functions[func]
        except:
            print('Unknow function at: ' + line)
            exit()
        if currentFunc.delay > tmpCycle:
            tmpCycle = currentFunc.delay
        currentFunc.computeCost(initialStocks)
    for stockValue in initialStocks.values():
        if stockValue < 0:
            print('Invalid operation at: ' + line)
            exit()
    localCycle += tmpCycle
    if localCycle != actualFileCycle:
        print('Cycle count is wrong at: ' + line)
        exit()
    for func in splitedLine:
        currentFunc = functions[func]
        currentFunc.computeReward(initialStocks)
    return localCycle

parseFile(data, initialStocks, processList, toOptimize)
functions = funcDictionaryBuild()
localCycle = 0
for line in output:
    if len(line) == 0:
        continue
    if line.startswith('State of stock after'):
        break
    localCycle = parseLine(line, functions, localCycle)
print('This output is correct.')
