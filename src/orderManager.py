from random import randint
from src.signalManager import SignalManager


class OrderManager():
    def __init__(self, initialCapital, strategyName, botName, currentInput, pair) -> None:
        self.initialCapital = initialCapital
        self.equity = initialCapital
        self.positionSize = 0
        self.positionAveragePrice = 0
        self.signalManager = SignalManager(strategyName, botName, currentInput, pair)
        self.lastSignal = 0

    def decider(self, marketData, equity, initialCapital, positionAveragePrice, positionSize):
        signal = self.signalManager.getSignal(marketData)
        if self.lastSignal == 0 or self.lastSignal == 2 or self.lastSignal == 4:
            if signal.longEnter and not signal.shortEnter:
                self.lastSignal = 1
                signal.side = "buy"
                return [1,signal]
            elif signal.shortEnter and not signal.longEnter:
                self.lastSignal = 3
                signal.side = "sell"
                return [3,signal]
            self.lastSignal = 0
            return [0,signal]
        elif self.lastSignal == 1:
            if signal.shortEnter:
                self.lastSignal = 3
                signal.side = "sell"
                return [3,signal]
            elif signal.longExit:
                self.lastSignal = 2
                signal.side = "buyEXIT"
                return [2,signal]
            return [0,signal]
        elif self.lastSignal == 3:
            if signal.longEnter:
                self.lastSignal = 1
                signal.side = "buy"
                return [1,signal]
            elif signal.shortExit:
                self.lastSignal = 4
                signal.side = "sellEXIT"
                return [4,signal]
        return [0,signal]

