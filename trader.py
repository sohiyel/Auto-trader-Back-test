from positionManager import PositionManager
from orderManager import OrderManager
from data import DataService

class Trader():
    def __init__ (self, symbol, timeFrame, startAt, endAt, initialCapital, orderManagers):
        self.pair = symbol
        self.startAt = startAt
        self.endAt = endAt
        self.initialCapital = initialCapital
        self.orderManagers = orderManagers
        self.orderManager = OrderManager(initialCapital)
        self.positionManager = PositionManager()
        self.dataService = DataService("spot", symbol, timeFrame, startAt, endAt)