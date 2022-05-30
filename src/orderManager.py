from src.signalManager import SignalManager
from src.logManager import LogService

class OrderManager():
    def __init__(self, initialCapital, strategyName,timeFrame, botName, currentInput, pair, settings, marketData="") -> None:
        self.initialCapital = initialCapital
        self.equity = initialCapital
        self.positionSize = 0
        self.positionAveragePrice = 0
        self.signalManager = SignalManager(strategyName, botName, currentInput, pair, settings, marketData)
        self.lastSignal = 0
        self.logService = LogService(__name__, settings)
        self.pair = pair
        self.strategyName = strategyName
        self.timeFrame = timeFrame
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        pts = {'pair': self.pair, 'timeFrame': self.timeFrame, 'strategyName': self.strategyName}
        self.logService.set_pts_formatter(pts)

    def decider(self, marketData, equity, initialCapital, positionAveragePrice, positionSize, timeStamp = ""):
        signal = self.signalManager.getSignal(marketData, timeStamp)
        if self.lastSignal == 0 or self.lastSignal == 2 or self.lastSignal == 4:
            if signal.longEnter and not signal.shortEnter:
                self.lastSignal = 1
                signal.side = "buy"
                return [1,signal]
            elif signal.shortEnter and not signal.longEnter:
                self.lastSignal = 3
                signal.side = "sell"
                return [3,signal]
            self.lastSignal = 0
            return [0,signal]
        elif self.lastSignal == 1:
            if signal.shortEnter:
                self.lastSignal = 3
                signal.side = "sell"
                return [3,signal]
            elif signal.longExit:
                self.lastSignal = 2
                signal.side = "sell"
                return [2,signal]
            return [0,signal]
        elif self.lastSignal == 3:
            if signal.longEnter:
                self.lastSignal = 1
                signal.side = "buy"
                return [1,signal]
            elif signal.shortExit:
                self.lastSignal = 4
                signal.side = "buy"
                return [4,signal]
        return [0,signal]

