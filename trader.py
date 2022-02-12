from positionManager import PositionManager
from orderManager import OrderManager
from data import DataService
from tfMap import tfMap
class Trader():
    def __init__ (self, symbol, timeFrame, startAt, endAt, initialCapital, orderManagers):
        self.pair = symbol
        self.dataService = DataService("spot", symbol, timeFrame, startAt, endAt)
        self.startAt = self.dataService.startAtTs
        self.endAt = self.dataService.endAtTs
        self.lastState = self.dataService.startAtTs
        self.initialCapital = initialCapital
        self.orderManagers = orderManagers
        self.orderManager = OrderManager(initialCapital)
        self.positionManager = PositionManager()
        self.timeFrame = timeFrame

        self.mainloop()

    def mainloop(self):
        for i in range(self.dataService.startAtTs,self.dataService.endAtTs, tfMap.array[self.timeFrame]*60):
            print (self.dataService.getCurrentData(i))