import importlib
from signals.single_strategy import SingleStrategy
from signals.bot_signal import BotSignal
import os

class SignalManager():
    def __init__(self, strategyName, botName, currentInput) -> None:
        if botName == "":
            self.signal = SingleStrategy(strategyName, currentInput)
        else:
            self.signal = BotSignal(botName, currentInput)

    def getSignal(self, marketData):
        signal = self.signal.decider(marketData)
        return signal
