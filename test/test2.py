import copy
import time
# import pydot
# import graphviz

openList = []

start = time.time()
class Func:
    def __init__(self, cost=None, reward=None, delay=1):
        self.cost = cost
        self.reward = reward
        self.delay = delay
        self.score = self.calculateScore()
        self.rewardOf = [] # Liste des functions qui ont besoin de ce que cette fonction produit
        self.costOf = [] # Liste des functions qui fournissent ce dont cette fonction a besoin

    def calculateScore(self):
        total = 0
        for cost in self.cost.values():
            total += cost * self.delay
        for reward in self.reward.values():
            total -= reward * self.delay
        return total

    def canBeComputed(self, items):
        for key, val in self.cost.items():
            if not items[key] >= val:
                return False
        return True


class potentialPath:
    def __init__(self):
        self.items = {'clock': 1,
                      'second': 0, 
                      'minute': 0,
                      'hour': 0,
                      'day': 0,
                      'year': 0,
                      'dream': 0}
        self.callStack = []
        self.amountCall = []
        self.totalCostTime = 0
        self.score = 0

    def updateRessources(self):
        for func, amount in zip(self.callStack, self.amountCall):
            for key in func.cost.keys():
                self.items[key] -= func.cost[key] * amount
            for key in func.reward.keys():
                self.items[key] += func.reward[key] * amount

    def addNode(self, func):
        self.callStack.append(func)


make_sec = Func({'clock': 1}, {'clock': 1, 'second': 1}, 1)
make_minute = Func({'second': 60}, {'minute': 1}, 6)
make_hour = Func({'minute': 60}, {'hour': 1}, 36)
make_day = Func({'hour': 24}, {'day': 1}, 86)
make_year = Func({'day': 365}, {'year': 1}, 365)
start_dream = Func({'minute': 1, 'clock': 1}, {'dream': 1}, 60)
start_dream_2 = Func({'minute': 1, 'dream': 1}, {'dream': 2}, 60)
dream_minute = Func({'second': 1, 'dream': 1}, {'minute': 1, 'dream': 2}, 1)
dream_hour = Func({'second': 1, 'dream': 2}, {'hour': 1, 'dream': 2}, 1)
dream_day = Func({'second': 1, 'dream': 3}, {'day': 1, 'dream': 3}, 1)
end_dream = Func({'dream': 3}, {'clock': 1}, 60)

function = (make_sec, make_minute, make_hour, make_day, make_year, start_dream, start_dream_2, dream_minute, dream_hour, dream_day, end_dream)
toOptimize = 'year'

for func1 in function:
    for func2 in function:
        if func1 is func2:
            continue
        for reward, cost in zip(func1.reward, func1.cost):
            if reward in func2.cost and func2 not in func1.rewardOf:
                func1.rewardOf.append(func2)
            if cost in func2.reward and func2 not in func1.costOf:
                func1.costOf.append(func2)


def searchForAvailableNodes(path):
    # Faire la recherche de chemin en prenant en compte uniquement le linkage des noeuds (sans notions de couts/recompenses)

firstPath = potentialPath()
while time.time() < start + 10:
    searchForAvailableNodes(firstPath)

# graph = pydot.Dot(graph_type='digraph')
# node1 = pydot.Node("make_sec")
# node2 = pydot.Node("make_minute")
# node3 = pydot.Node("make_hour")
# node4 = pydot.Node("make_day")
# node5 = pydot.Node("make_year")
# node6 = pydot.Node("start_dream")
# node7 = pydot.Node("start_dream_2")
# node8 = pydot.Node("dream_minute")
# node9 = pydot.Node("dream_hour")
# node10 = pydot.Node("dream_day")
# node11 = pydot.Node("end_dream")
# graph.add_node(node1)
# graph.add_node(node2)
# graph.add_node(node3)
# graph.add_node(node4)
# graph.add_node(node5)
# graph.add_node(node6)
# graph.add_node(node7)
# graph.add_node(node8)
# graph.add_node(node9)
# graph.add_node(node10)
# graph.add_node(node11)

# graph.add_edge(pydot.Edge(node1, node2))
# graph.add_edge(pydot.Edge(node1, node8))
# graph.add_edge(pydot.Edge(node1, node9))
# graph.add_edge(pydot.Edge(node1, node10))

# graph.add_edge(pydot.Edge(node2, node3))
# graph.add_edge(pydot.Edge(node2, node6))
# graph.add_edge(pydot.Edge(node2, node7))

# graph.add_edge(pydot.Edge(node3, node4))

# graph.add_edge(pydot.Edge(node4, node5))

# graph.add_edge(pydot.Edge(node6, node7))
# graph.add_edge(pydot.Edge(node6, node8))
# graph.add_edge(pydot.Edge(node6, node9))
# graph.add_edge(pydot.Edge(node6, node10))
# graph.add_edge(pydot.Edge(node6, node11))

# graph.add_edge(pydot.Edge(node7, node8))
# graph.add_edge(pydot.Edge(node7, node9))
# graph.add_edge(pydot.Edge(node7, node10))
# graph.add_edge(pydot.Edge(node7, node11))

# graph.add_edge(pydot.Edge(node8, node3))
# graph.add_edge(pydot.Edge(node8, node6))
# graph.add_edge(pydot.Edge(node8, node7))
# graph.add_edge(pydot.Edge(node8, node9))
# graph.add_edge(pydot.Edge(node8, node10))
# graph.add_edge(pydot.Edge(node8, node11))

# graph.add_edge(pydot.Edge(node9, node4))
# graph.add_edge(pydot.Edge(node9, node7))
# graph.add_edge(pydot.Edge(node9, node8))
# graph.add_edge(pydot.Edge(node9, node10))
# graph.add_edge(pydot.Edge(node9, node11))

# graph.add_edge(pydot.Edge(node10, node5))
# graph.add_edge(pydot.Edge(node10, node7))
# graph.add_edge(pydot.Edge(node10, node8))
# graph.add_edge(pydot.Edge(node10, node9))
# graph.add_edge(pydot.Edge(node10, node11))

# graph.add_edge(pydot.Edge(node11, node1))

# graph.write_png('test/example2_graph.png')

# def getAvailableNode(actualPath):
#     validPath = []
#     for func in function:
#         isOK = True
#         for cost in func.cost.keys():
#             if actualPath.items[cost] > 0:
#                 continue
#             else:
#                 isOK = False
#                 break
#         if isOK and func not in actualPath.path:
#             validPath.append(func)
#     return validPath


# def searchPath(actualPath):
#     tmp = getAvailableNode(actualPath)
#     for node in tmp:
#         newPath = copy.copy(actualPath)
#         newPath.path.append(node)
#         newPath.updateRessources()
#         openList.append(newPath)
#     openList.sort(key=lambda potentialPath: potentialPath.score, reverse=True)


# bestPath = []
# toOptimize = 'year'
# actualPath = potentialPath()
# while True:
#     # getAvailableNode(actualPath)
#     bestPath.append(searchPath(actualPath))
#     print(bestPath)
