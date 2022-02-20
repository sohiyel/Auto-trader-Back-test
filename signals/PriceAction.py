from strategies.price_action01 import PriceAction01
from signalClass import SignalClass

class PriceAction():
    def __init__(self) -> None:
        self.lastSignal = 0
        self.marketData = []
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        if len(self.marketData) < 5:
            return SignalClass()
        strategy = PriceAction01()
        signal = strategy.decider(self.marketData)
        return signal
        # print(decision)
        


