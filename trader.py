import pandas
from positionManager import PositionManager
from orderManager import OrderManager
from data import DataService
from portfolioManager import PortfolioManager
from tfMap import tfMap
from datetime import datetime
from pytz import timezone
import os



class Trader():
    def __init__ (self,market, symbol, timeFrame, startAt, endAt, initialCapital, orderManagers):
        self.pair = symbol
        self.dataService = DataService(market, symbol, timeFrame, startAt, endAt)
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
        self.balances = []
        self.mainloop()

    def openPosition(self, type, price, volume):
        if len( self.positionManager.openPositions ) == 0:
                self.positionManager.openPosition(self.pair, type, price, volume, self.lastState)
                self.portfolioManager.openPosition(volume, price, self.positionManager.openPositions[0].commission)
        elif len( self.positionManager.openPositions ) == 1:
            if self.positionManager.openPositions[0].type == type:
                self.positionManager.addVolume(price, volume)
                self.portfolioManager.addVolume(volume, price, self.positionManager.openPositions[0].commission)
            else:
                lastPrice = self.positionManager.closePosition(self.lastState)
                self.portfolioManager.closePosition(lastPrice, self.positionManager.closedPositions[-1].commission)
                if self.positionManager.closedPositions[-1].profit > 0:
                    self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
                else:
                    self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
                self.balances.append(self.portfolioManager.balance)
                self.positionManager.openPosition(self.pair, type, price, volume, self.lastState)
                self.portfolioManager.openPosition(volume, price, self.positionManager.openPositions[0].commission)

    def closePosition(self):
        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.closePosition(self.lastState)
            self.portfolioManager.closePosition(lastPrice, self.positionManager.closedPositions[-1].commission)
            if self.positionManager.closedPositions[-1].profit > 0:
                self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
            else:
                self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
            self.balances.append(self.portfolioManager.balance)

    def processOrders(self, choice, price, volume):
        if choice == 0:
            pass

        elif choice == 1:
            self.openPosition("Long", price, volume)
            
        elif choice == 2:
            self.closePosition()

        elif choice == 3:
            self.openPosition("SHORT", price, volume)
            
        elif choice == 4:
            self.closePosition()



    def mainloop(self):
        global balances
        for i in range(self.dataService.startAtTs,self.dataService.endAtTs, tfMap.array[self.timeFrame]*60):
            if self.portfolioManager.balance <= 0:
                break
            self.lastState = i
            self.lastCandle = self.dataService.getCurrentData(i)
            # print(self.lastCandle['close'].values[0])
            self.positionManager.updatePositions(self.lastCandle['close'].values[0])
            choice = self.orderManager.decider(self.lastCandle, self.portfolioManager.equity, self.portfolioManager.balance, self.positionManager.positionAveragePrice(), self.positionManager.positionSize())
            self.processOrders(choice, self.lastCandle["close"].values[0], 1)
            # print(self.portfolioManager.balance)

            self.portfolioManager.calcPoL()

            clear = lambda: os.system('cls')
            clear()

            df = pandas.DataFrame.from_records([position.to_dict() for position in self.positionManager.openPositions])
            df['Balance'] = self.portfolioManager.balance
            print(df)

        self.processOrders(4, self.lastCandle["close"].values[0], 1)
        print (self.portfolioManager.numProfits, self.portfolioManager.numLosses)
        print (self.portfolioManager.profit, self.portfolioManager.loss)
        print (self.portfolioManager.pol)
        print (self.portfolioManager.balance)
        print (datetime.fromtimestamp(i, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S'))
        print( len(self.balances))

        df = pandas.DataFrame.from_records([position.to_dict() for position in self.positionManager.closedPositions])
        print(df)
