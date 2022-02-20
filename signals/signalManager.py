import importlib
import os

class SignalManager():
    def __init__(self, signalName) -> None:
        signals = importlib.import_module("signals."+signalName)
        SignalClass = getattr(signals, signalName)
        self.signal = SignalClass()

    def getSignal(self, marketData):
        return self.signal.decider(marketData)
