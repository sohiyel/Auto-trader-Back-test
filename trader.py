import pandas
from positionManager import PositionManager
from orderManager import OrderManager
from data import DataService
from portfolioManager import PortfolioManager
from tfMap import tfMap
from datetime import datetime
from pytz import timezone
import os
from plotter import Plotter


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
        self.plotter =  Plotter(self.pair + "_" + str(self.startAt) + "_" + str(self.endAt) + "_" + self.timeFrame + ".csv" )
        self.lastCandle = ""
        self.balances = []
        self.equities = []
        self.mainloop()

    def openPosition(self, type, price, volume, commission):
        if len( self.positionManager.openPositions ) == 0:
            if self.portfolioManager.openPosition(volume, price, commission):
                self.positionManager.openPosition(self.pair, type, price, volume, self.lastState)
        elif len( self.positionManager.openPositions ) == 1:
            if self.positionManager.openPositions[0].type == type:
                if self.portfolioManager.addVolume(volume, price, commission):
                    self.positionManager.addVolume(price, volume)
            else:
                lastPrice = self.positionManager.closePosition(self.lastState)
                self.portfolioManager.closePosition(lastPrice, commission)
                if self.positionManager.closedPositions[-1].profit > 0:
                    self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
                else:
                    self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
                
                self.balances.append(self.portfolioManager.balance)
                if self.portfolioManager.openPosition(volume, price, commission):
                    self.positionManager.openPosition(self.pair, type, price, volume, self.lastState)
                

    def closePosition(self, commission):
        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.closePosition(self.lastState)
            self.portfolioManager.closePosition(lastPrice, commission)
            if self.positionManager.closedPositions[-1].profit > 0:
                self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
            else:
                self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
            self.balances.append(self.portfolioManager.balance)

    def processOrders(self, choice, price, volume, commission):
        if choice == 0:
            pass

        elif choice == 1:
            self.openPosition("LONG", price, volume, commission)
            
        elif choice == 2:
            self.closePosition(commission)

        elif choice == 3:
            self.openPosition("SHORT", price, volume, commission)
            
        elif choice == 4:
            self.closePosition(commission)

        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.calcEquity()
            self.equities.append(self.portfolioManager.updateEquity(lastPrice))



    def mainloop(self):
        global balances
        for i in range(self.dataService.startAtTs,self.dataService.endAtTs, tfMap.array[self.timeFrame]*60):
            if self.portfolioManager.balance <= 0:
                self.processOrders(4, self.lastCandle["close"].values[0], 1, 0)
                self.portfolioManager.balance = 0
                break
            self.lastState = i
            self.lastCandle = self.dataService.getCurrentData(i)
            # print(self.lastCandle['close'].values[0])
            self.positionManager.updatePositions(self.lastCandle['close'].values[0])
            choice = self.orderManager.decider(self.lastCandle, self.portfolioManager.equity, self.portfolioManager.balance, self.positionManager.positionAveragePrice(), self.positionManager.positionSize())
            self.processOrders(choice, self.lastCandle["close"].values[0], 1, 0)
            # print(self.portfolioManager.balance)

            self.portfolioManager.calcPoL()

            clear = lambda: os.system('cls')
            clear()

            df = pandas.DataFrame.from_records([position.to_dict() for position in self.positionManager.openPositions])
            df['Balance'] = self.portfolioManager.balance
            df['Equity'] = self.portfolioManager.equity
            print(df)

        self.processOrders(4, self.lastCandle["close"].values[0], 1, 0)
        print (self.portfolioManager.numProfits, self.portfolioManager.numLosses)
        print (self.portfolioManager.profit, self.portfolioManager.loss)
        print (self.portfolioManager.pol)
        print (self.portfolioManager.balance)
        print (datetime.fromtimestamp(i, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S'))
        print( len(self.balances))

        df = pandas.DataFrame.from_records([position.to_dict() for position in self.positionManager.closedPositions])
        df['Balance'] = self.balances
        print(df)

        self.plotter.writeDFtoFile(df)
