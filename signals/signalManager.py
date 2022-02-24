import importlib
from signals.single_strategy import SingleStrategy
from signals.bot_signal import BotSignal
import os

class SignalManager():
    def __init__(self, strategyName, botName, pair, timeFrame) -> None:
        if botName == "":
            self.signal = SingleStrategy(strategyName, timeFrame, pair)
        else:
            self.signal = BotSignal(botName, timeFrame, pair)

    def getSignal(self, marketData):
        signal = self.signal.decider(marketData)
        return signal
