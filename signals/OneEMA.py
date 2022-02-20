from strategies.one_ema import OneEMA

class OneEMA():
    def __init__(self, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        if len(self.marketData) < 5:
            return 0
        strategy = OneEMA(self.timeFrame, self.pair)
        signal = strategy.decider(self.marketData)
        # print(decision)
        return signal