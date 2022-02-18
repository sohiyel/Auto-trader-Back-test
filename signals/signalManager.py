from .price_action_signal import PriceActionSignal

class SignalManager():
    def __init__(self) -> None:
        self.signal = PriceActionSignal()

    def getSignal(self, marketData):
        return self.signal.decider(marketData)
