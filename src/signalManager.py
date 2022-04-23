import importlib
from src.singleStrategy import SingleStrategy
from src.botSignal import BotSignal
import os

class SignalManager():
    def __init__(self, strategyName, botName, currentInput, pair, settings) -> None:
        if botName == "":
            self.signal = SingleStrategy(strategyName, currentInput, pair, settings)
        else:
            self.signal = BotSignal(botName, currentInput, pair, settings)

    def getSignal(self, marketData):
        signal = self.signal.decider(marketData)
        return signal
