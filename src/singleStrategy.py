import importlib
from src.logManager import get_logger

class SingleStrategy():
    def __init__(self, strategyName, currentInput, pair, settings, marketData) -> None:
        self.lastSignal = 0
        self.marketData = []
        self.logger = get_logger(__name__, settings)
        try:
            strategies = importlib.import_module(settings.STRATEGIES_MODULE_PATH+strategyName)
            self.StrategyClass = getattr(strategies, strategyName)
            self.strategy = self.StrategyClass(currentInput, pair, marketData)
        except:
            self.logger.error(f"Cannot import {strategyName}!")
        
    def decider(self, marketData, timeStamp):
        self.marketData = marketData
        signal = self.strategy.decider(self.marketData, timeStamp)
        return signal