from positionManager import PositionManager
from orderManager import OrderManager
from data import DataService
from portfolioManager import PortfolioManager
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
        self.portfolioManager = PortfolioManager(initialCapital)
        self.timeFrame = timeFrame
        self.lastCandle = ""

        self.mainloop()

    def processOrder(self, choice, price, volume):
        if choice == 0:
            pass
        elif choice == 1:
            self.positionManager.openPosition(self.pair, "LONG", price, volume, self.lastState)
            self.portfolioManager.balance -= price * volume
        elif choice == 2:
            profit = self.positionManager.closePosition(self.lastState)
            self.portfolioManager.balance += profit
        elif choice == 3:
            self.positionManager.openPosition(self.pair, "SHORT", price, volume, self.lastState)
            self.portfolioManager.balance -= price * volume
        elif choice == 4:
            profit = self.positionManager.closePosition(self.lastState)
            self.portfolioManager.balance += profit



    def mainloop(self):
        for i in range(self.dataService.startAtTs,self.dataService.endAtTs, tfMap.array[self.timeFrame]*60):
            self.lastState = i
            self.lastCandle = self.dataService.getCurrentData(i)
            # print(self.lastCandle['close'].values[0])
            self.positionManager.updatePositions(self.lastCandle['close'].values[0])
            choice = self.orderManager.decider(self.lastCandle, self.portfolioManager.equity, self.portfolioManager.balance, self.positionManager.positionAveragePrice(), self.positionManager.positionSize())
            self.processOrder(choice, self.lastCandle["close"].values[0], 0.01)
            print(self.portfolioManager.balance)