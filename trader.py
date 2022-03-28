from logging import currentframe
import pandas as pd
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
    def __init__ (self, index, exchange, market = 'spot'):
        self.exchange = exchange
        self.pair = index.pair
        self.startAt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.endAt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        historyNeeded = index.calc_history_needed()
        self.historyNeeded = int(historyNeeded)
        self.dataService = DataService(market, index.pair, index.timeFrame, self.startAt, self.endAt, historyNeeded)
        self.startAtTS = self.dataService.startAtTs
        self.endAtTS = self.dataService.endAtTs
        self.lastState = self.dataService.startAtTs
        self.strategyName = index.strategyName
        self.botName = index.botName
        self.portfolioManager = PortfolioManager(1,exchange)
        self.initialCapital = self.portfolioManager.get_balance()
        self.orderManager = OrderManager(self.initialCapital, index.strategyName, index.botName, index.inputs, index.pair)
        self.positionManager = PositionManager()
        self.timeFrame = index.timeFrame
        self.lastCandle = ""
        self.volume = index.amount
        self.currentInput = index
        choice, signal = self.orderManager.decider(self.dataService.dataFrame.iloc[:],
                                                        self.portfolioManager.equity,
                                                        self.portfolioManager.balance,
                                                        self.positionManager.positionAveragePrice(),
                                                        self.positionManager.positionSize())

    def openPosition(self, signal, commission):
        if len( self.positionManager.openPositions ) == 0:
            if self.portfolioManager.open_position(signal.volume, signal.price, commission):
                self.positionManager.openPosition(signal, self.lastState)
        elif len( self.positionManager.openPositions ) == 1:
            if self.positionManager.openPositions[0].type == signal.type:
                if self.portfolioManager.add_volume(signal.volume, signal.price, commission):
                    self.positionManager.addVolume(signal.price, signal.volume)
            else:
                lastPrice = self.positionManager.closePosition(self.lastState)
                self.portfolioManager.close_position(lastPrice, commission)
                if self.positionManager.closedPositions[-1].profit > 0:
                    self.portfolioManager.add_profit(self.positionManager.closedPositions[-1].profit)
                else:
                    self.portfolioManager.add_loss(self.positionManager.closedPositions[-1].profit)
                
                self.portfolioManager.balances.append(self.portfolioManager.balance)
                if self.portfolioManager.open_position(signal.volume, signal.price, commission):
                    self.positionManager.openPosition(signal, self.lastState)
                

    def closePosition(self, commission):
        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.closePosition(self.lastState)
            self.portfolioManager.close_position(lastPrice, commission)
            if self.positionManager.closedPositions[-1].profit > 0:
                self.portfolioManager.add_profit(self.positionManager.closedPositions[-1].profit)
            else:
                self.portfolioManager.add_loss(self.positionManager.closedPositions[-1].profit)
            self.portfolioManager.balances.append(self.portfolioManager.balance)

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
            self.portfolioManager.equities.append(self.portfolioManager.update_equity(lastPrice))



    def mainloop(self):
        while True:
            if self.portfolioManager.get_equity():
                if self.portfolioManager.equity <= 0:
                    self.processOrders(4, None, 0.0006)
                    self.portfolioManager.balance = 0
                    break
            choice, signal = self.orderManager.decider(self.lastCandle.iloc[0],
                                                        self.portfolioManager.equity,
                                                        self.portfolioManager.balance,
                                                        self.positionManager.positionAveragePrice(),
                                                        self.positionManager.positionSize())
            time.sleep(tfMap.array[self.timeFrame]*60)

            # self.lastState = i
            # self.lastCandle = self.dataService.getCurrentData(i)
            # checkContinue = self.positionManager.updatePositions(self.lastCandle['close'].values[0], self.lastState)
            # if not checkContinue :
            #     self.processOrders(4, None, 0.00060)
            #     continue

            # choice, signal = self.orderManager.decider(self.lastCandle.iloc[0], self.portfolioManager.equity, self.portfolioManager.balance, self.positionManager.positionAveragePrice(), self.positionManager.positionSize())
            # self.processOrders(choice, signal, 0.00060)
            # self.portfolioManager.calc_poL()

        # self.processOrders(4, None, 0.0006)