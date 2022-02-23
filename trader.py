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
import time


class Trader():
    def __init__ (self,market, pair, timeFrame, startAt, endAt, initialCapital, strategyName, botName, volume):
        self.pair = pair
        self.dataService = DataService(market, pair, timeFrame, startAt, endAt)
        self.startAt = self.dataService.startAtTs
        self.endAt = self.dataService.endAtTs
        self.lastState = self.dataService.startAtTs
        self.initialCapital = initialCapital
        self.strategyName = strategyName
        self.orderManager = OrderManager(initialCapital, strategyName, botName, timeFrame, pair)
        self.positionManager = PositionManager()
        self.portfolioManager = PortfolioManager(initialCapital)
        self.timeFrame = timeFrame
        self.plotter =  Plotter(self.pair + "_" + str(self.startAt) + "_" + str(self.endAt) + "_" + self.timeFrame + ".csv" )
        self.lastCandle = ""
        self.balances = []
        self.equities = []
        self.volume = volume
        self.mainloop()

    def openPosition(self, signal, commission):
        if len( self.positionManager.openPositions ) == 0:
            if self.portfolioManager.openPosition(signal.volume, signal.price, commission):
                self.positionManager.openPosition(signal, self.lastState)
        elif len( self.positionManager.openPositions ) == 1:
            if self.positionManager.openPositions[0].type == signal.type:
                if self.portfolioManager.addVolume(signal.volume, signal.price, commission):
                    self.positionManager.addVolume(signal.price, signal.volume)
            else:
                lastPrice = self.positionManager.closePosition(self.lastState)
                self.portfolioManager.closePosition(lastPrice, commission)
                if self.positionManager.closedPositions[-1].profit > 0:
                    self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
                else:
                    self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
                
                self.balances.append(self.portfolioManager.balance)
                if self.portfolioManager.openPosition(signal.volume, signal.price, commission):
                    self.positionManager.openPosition(signal, self.lastState)
                

    def closePosition(self, commission):
        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.closePosition(self.lastState)
            self.portfolioManager.closePosition(lastPrice, commission)
            if self.positionManager.closedPositions[-1].profit > 0:
                self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
            else:
                self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
            self.balances.append(self.portfolioManager.balance)

    def processOrders(self, choice, signal, commission ):
        if choice == 0:
            pass

        elif choice == 1:
            if signal:
                self.openPosition(signal, commission)
            
        elif choice == 2:
            self.closePosition(commission)

        elif choice == 3:
            if signal:
                self.openPosition(signal, commission)
            
        elif choice == 4:
            self.closePosition(commission)

        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.calcEquity()
            self.equities.append(self.portfolioManager.updateEquity(lastPrice))



    def mainloop(self):
        global balances
        start_time = time.time()
        for i in range(self.dataService.startAtTs,self.dataService.endAtTs, tfMap.array[self.timeFrame]*60):
            if self.portfolioManager.equity <= 0:
                self.processOrders(4, None, 0.0006)
                self.portfolioManager.balance = 0
                break
            self.lastState = i
            self.lastCandle = self.dataService.getCurrentData(i)
            # print(self.lastCandle['close'].values[0])
            checkContinue = self.positionManager.updatePositions(self.lastCandle['close'].values[0], self.lastState)
            if not checkContinue :
                self.processOrders(4, None, 0.00060)
                continue

            choice, signal = self.orderManager.decider(self.lastCandle.iloc[0], self.portfolioManager.equity, self.portfolioManager.balance, self.positionManager.positionAveragePrice(), self.positionManager.positionSize())
            self.processOrders(choice, signal, 0.00060)
            # print(self.portfolioManager.balance)

            self.portfolioManager.calcPoL()

            # clear = lambda: os.system('cls')
            # clear()

            # df = pandas.DataFrame.from_records([position.to_dict() for position in self.positionManager.openPositions])
            # df['Balance'] = self.portfolioManager.balance
            # df['Equity'] = self.portfolioManager.equity
            # print(df)

        self.processOrders(4, None, 0.0006)
        print("--- %s seconds ---" % (time.time() - start_time))

        print (self.portfolioManager.numProfits, self.portfolioManager.numLosses)
        print (self.portfolioManager.profit, self.portfolioManager.loss)
        print (self.portfolioManager.pol)
        print (self.portfolioManager.balance)
        print (datetime.fromtimestamp(i, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S'))
        print( len(self.balances))

        df = pandas.DataFrame.from_records([position.to_dict() for position in self.positionManager.closedPositions])
        df['Balance'] = self.balances
        print(df)
        print("--- %s seconds ---" % (time.time() - start_time))

        self.plotter.writeDFtoFile(df)
        print("--- %s seconds ---" % (time.time() - start_time))

