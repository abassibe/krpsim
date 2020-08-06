from random import seed, randint, shuffle

bestDelay = 2147483647
savePath = list()
seed(None)

class Func:
    def __init__(self, cost=None, reward=None, delay=1):
        self.cost = cost
        self.reward = reward
        self.delay = delay

    def can_process(self, items, amountTime):
        i = 0
        tmp = items
        while i < amountTime:
            for key, cost in self.cost.items():
                if tmp[key] < cost:
                    return False
                tmp[key] -= cost
            for key, reward in self.reward.items():
                tmp[key] += reward
            i += 1
        return True

    def processing(self, items, totalCostTime, amountTime):
        for key, value in self.cost.items():
            items[key] -= value * amountTime
        for key, value in self.reward.items():
            items[key] += value * amountTime
        totalCostTime += self.delay
        return totalCostTime


class Individual:
    def __init__(self, gen):
        self.items = {'clock': 1,
                      'second': 0, 
                      'minute': 0,
                      'hour': 0,
                      'day': 0,
                      'year': 0,
                      'dream': 0,}
        self.totalCostTime = 0
        self.gen = list()
        self.amountGen = gen
        self.score = 0

    def makeGen(self):
        i = 0
        genPool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        shuffle(genPool)
        while i < self.amountGen * 2:
            if i % 2 == 0 and randint(0, 5) != 1:
                self.gen.append(genPool.pop())
            elif i % 2 == 1:
                self.gen.append(randint(1, 255))
            else:
                self.gen.append(-1)
            i += 1
    
    def startProcess(self):
        i = 0
        while i < self.amountGen * 2:
            if function[self.gen[i]].can_process(self.items, self.gen[i + 1]):
                self.totalCostTime = function[self.gen[i]].processing(self.items, self.totalCostTime, self.gen[i + 1])
            else:
                break
            i += 2

    def calculateScore(self):
        for key, value in self.items.items():
            if key == 'clock':
                self.score += value * 1
            elif key == 'second':
                self.score += value * 2
            elif key == 'minute':
                self.score += value * 3
            elif key == 'hour':
                self.score += value * 4
            elif key == 'day':
                self.score += value * 5
            elif key == 'year':
                self.score += value * 20
            elif key == 'dream':
                self.score += value * 10


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

def meanOfIndividuals(ppls):
    total = 0
    for ppl in ppls:
        total += ppl.score
    return total / len(ppls)


def doSomeSecks(population):
    males = []
    females = []
    for individuals in population:
        pass
        # trier par score le plus élevé
        # faire 2 liste male/female
        # les faire se reproduire
        # remplir les 2/3 de la liste restante (sur 100) avec des mutations et le reste avec de nouveaux individus
 

ppls = [Individual(11) for _ in range(100)]
while True:
    for ppl in ppls:
        ppl.makeGen()
        print(ppl.gen)
        ppl.startProcess()
        ppl.calculateScore()
        print(ppl.items)
    averageScore = meanOfIndividuals(ppls)
    print(averageScore)
    i = 0
    while i < len(ppls):
        if ppls[i].score < averageScore:
            ppls.remove(ppls[i])
            continue
        i += 1
    print("-------------")
    print(ppl.items)
    break
