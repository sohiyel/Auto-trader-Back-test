import importlib
from src.logManager import LogService

class SingleStrategy():
    def __init__(self, strategyName, currentInput, pair, settings, marketData) -> None:
        self.lastSignal = 0
        self.marketData = []
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        pts = {'pair': pair, 'timeFrame': 'NaN', 'strategyName': strategyName}
        self.logService.set_pts_formatter(pts)
        try:
            strategies = importlib.import_module(settings.STRATEGIES_MODULE_PATH+strategyName)
            self.StrategyClass = getattr(strategies, strategyName)
            self.strategy = self.StrategyClass(currentInput, pair, marketData, settings)
        except:
            self.logger.error(f"Cannot import {settings.STRATEGIES_MODULE_PATH+strategyName}!")
            raise FileNotFoundError(f"Cannot import {settings.STRATEGIES_MODULE_PATH+strategyName}!")
        
    def decider(self, marketData, timeStamp):
        signal = self.strategy.decider(marketData, timeStamp)
        return signal