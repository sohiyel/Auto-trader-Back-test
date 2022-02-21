from strategies.one_ema import OneEMAStrategy
from signalClass import SignalClass

class OneEMA():
    def __init__(self, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        strategy = OneEMAStrategy(self.timeFrame, self.pair)
        signal = strategy.decider(self.marketData)
        # print(self.marketData[-1])
        return signal