import importlib
from src.logManager import LogService

class SingleStrategy():
    def __init__(self, strategyName, currentInput, pair, settings, marketData) -> None:
        self.lastSignal = 0
        self.marketData = []
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        try:
            strategies = importlib.import_module(settings.STRATEGIES_MODULE_PATH+strategyName)
            self.StrategyClass = getattr(strategies, strategyName)
            self.strategy = self.StrategyClass(currentInput, pair, marketData, settings)
        except:
            self.logger.error(f"Cannot import {settings.STRATEGIES_MODULE_PATH+strategyName}!")
        
    def decider(self, marketData, timeStamp):
        self.marketData = marketData
        signal = self.strategy.decider(self.marketData, timeStamp)
        return signal