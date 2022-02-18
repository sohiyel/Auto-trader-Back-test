from base64 import decode
from pydoc import describe
from signalManager import SignalManager
from ..strategies.price_action01 import PriceAction01

class Signal01(SignalManager):
    def __init__(self) -> None:
        super().__init__()
        self.strategy = PriceAction01()
        self.lastSignal = 0
        self.marketData = []
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        if len(self.marketData) < 5:
            return 0
        decision = self.strategy.decider(self.marketData)
        position = decision['longEnt'] + decision['longExt'] + decision['shortEnt'] + decision['shortExt']
        

