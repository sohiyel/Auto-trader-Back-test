import importlib
class SingleStrategy():
    def __init__(self, strategyName, currentInput, pair, settings, marketData) -> None:
        self.lastSignal = 0
        self.marketData = []
        strategies = importlib.import_module(settings.STRATEGIES_MODULE_PATH+strategyName)
        self.StrategyClass = getattr(strategies, strategyName)
        self.strategy = self.StrategyClass(currentInput, pair, marketData)
        
    def decider(self, marketData, timeStamp):
        self.marketData = marketData
        signal = self.strategy.decider(self.marketData, timeStamp)
        # print(self.marketData[-1])
        return signal