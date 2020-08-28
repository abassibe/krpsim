class Ressource():
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.linkedFunction = []

    def addLink(self, function):
        self.linkedFunction.append(function)

    def addValue(self, value):
        self.quantity += value
