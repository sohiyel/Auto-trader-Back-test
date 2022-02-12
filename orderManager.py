from random import randint


class OrderManager():
    def __init__(self, initialCapital) -> None:
        self.initialCapital = initialCapital
        self.equity = initialCapital
        self.positionSize = 0
        self.positionAveragePrice = 0

    def decider(self, marketData, equity, initialCapital, positionAveragePrice, positionSize):
        choice = randint(0,4)
        return choice

