import importlib

class SingleStrategy():
    def __init__(self, strategyName, currentInput, pair) -> None:
        self.lastSignal = 0
        self.marketData = []
        strategies = importlib.import_module("strategies."+strategyName)
        self.StrategyClass = getattr(strategies, strategyName)
        self.strategy = self.StrategyClass(currentInput, pair)
        
    def decider(self, marketData):
        self.marketData.extend(marketData)
        signal = self.strategy.decider(self.marketData)
        # print(self.marketData[-1])
        return signal