import importlib

class SingleStrategy():
    def __init__(self, strategyName, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        strategies = importlib.import_module("strategies."+strategyName)
        self.StrategyClass = getattr(strategies, strategyName)
        self.timeFrame = timeFrame
        self.pair = pair
        
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        self.strategy = self.StrategyClass(self.timeFrame, self.pair)
        signal = self.strategy.decider(self.marketData)
        # print(self.marketData[-1])
        return signal