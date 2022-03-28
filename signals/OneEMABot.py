from strategies.OneEMA import OneEMA

class OneEMABot():
    def __init__(self, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        
    def decider(self, marketData):
        self.marketData.extend(marketData)
        strategy = OneEMA(self.timeFrame, self.pair)
        signal = strategy.decider(self.marketData)
        # print(self.marketData[-1])
        return signal