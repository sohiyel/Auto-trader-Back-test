import importlib
from signals.single_strategy import SingleStrategy
import os

class SignalManager():
    def __init__(self, strategyName, botName, pair, timeFrame) -> None:
        if botName == "":
            self.signal = SingleStrategy(strategyName, timeFrame, pair)
        else:
            signals = importlib.import_module("signals."+botName)
            SignalClass = getattr(signals, botName)
            self.signal = SignalClass(timeFrame, pair)

    def getSignal(self, marketData):
        signal = self.signal.decider(marketData)
        return signal
