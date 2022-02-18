from random import randint
from signals.signalManager import SignalManager


class OrderManager():
    def __init__(self, initialCapital) -> None:
        self.initialCapital = initialCapital
        self.equity = initialCapital
        self.positionSize = 0
        self.positionAveragePrice = 0
        self.signalManager = SignalManager()

    def decider(self, marketData, equity, initialCapital, positionAveragePrice, positionSize):
        choice = self.signalManager.getSignal(marketData)
        return choice

