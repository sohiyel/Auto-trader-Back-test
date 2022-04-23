import importlib
class SingleStrategy():
    def __init__(self, strategyName, currentInput, pair, settings) -> None:
        self.lastSignal = 0
        self.marketData = []
        strategies = importlib.import_module(settings.STRATEGIES_MODULE_PATH+strategyName)
        self.StrategyClass = getattr(strategies, strategyName)
        self.strategy = self.StrategyClass(currentInput, pair)
        
    def decider(self, marketData):
        self.marketData = marketData
        signal = self.strategy.decider(self.marketData)
        # print(self.marketData[-1])
        return signal