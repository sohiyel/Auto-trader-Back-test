from logging import currentframe
import pandas as pd
from src.positionManager import PositionManager
from src.orderManager import OrderManager
from src.data import DataService
from src.portfolioManager import PortfolioManager
from src.tfMap import tfMap
from datetime import datetime
from pytz import timezone
import os
from src.plotter import Plotter
import time


class Trader():
    def __init__ (self, index, exchange, settings, market = 'futures'):
        self.settings = settings
        self.exchange = exchange
        self.pair = index.pair
        self.side = index.side
        self.startAt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        historyNeeded = index.calc_history_needed()
        self.historyNeeded = int(historyNeeded)
        self.endAt = datetime.fromtimestamp(time.time() - historyNeeded, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
        self.dataService = DataService(market, index.pair, index.timeFrame, self.startAt, self.endAt, historyNeeded, settings)
        self.startAtTS = self.dataService.startAtTs
        self.endAtTS = self.dataService.endAtTs
        self.lastState = self.dataService.startAtTs
        self.strategyName = index.strategyName
        self.botName = index.botName
        self.portfolioManager = PortfolioManager(index.pair,1, settings, exchange)
        self.initialCapital = self.portfolioManager.get_equity()
        self.orderManager = OrderManager(self.initialCapital, index.strategyName, index.botName, index.inputs, index.pair, settings)
        self.timeFrame = index.timeFrame
        self.lastCandle = ""
        self.volume = index.amount
        self.ratioAmount = index.ratioAmount
        self.leverage = index.leverage
        self.positionManager = PositionManager(self.portfolioManager.initialCapital, self.pair, self.volume, self.ratioAmount, self.timeFrame, self.strategyName, self.botName, self.leverage,settings, exchange)
        self.positionManager.sync_positions()
        self.currentInput = index
        self.df = ""

    def openPosition(self, signal, commission):
        if len( self.positionManager.openPositions ) == 0:
            if self.portfolioManager.open_position(signal.volume, signal.price, commission):
                self.positionManager.open_position(signal, self.lastState)
        elif len( self.positionManager.openPositions ) == 1:
            if self.positionManager.openPositions[0].side == signal.side:
                if self.portfolioManager.add_volume(signal.volume, signal.price, commission):
                    self.positionManager.add_volume(signal.price, signal.volume)
            else:
                lastPrice = self.positionManager.close_position(self.lastState)
                self.portfolioManager.close_position(lastPrice, commission)
                if self.positionManager.closedPositions[-1].profit > 0:
                    self.portfolioManager.add_profit(self.positionManager.closedPositions[-1].profit)
                else:
                    self.portfolioManager.add_loss(self.positionManager.closedPositions[-1].profit)
                
                self.portfolioManager.balances.append(self.portfolioManager.balance)
                if self.portfolioManager.open_position(signal.volume, signal.price, commission):
                    self.positionManager.open_position(signal, self.lastState)
                

    def closePosition(self, commission):
        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.close_position(self.lastState)
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
            if self.side == "long" or self.side == "both":
                if signal:
                    self.openPosition(signal, commission)
            
        elif choice == 2:
            if self.side == "long" or self.side == "both":
                if signal:
                    self.closePosition(commission)

        elif choice == 3:
            if self.side == "short" or self.side == "both":
                if signal:
                    self.openPosition(signal, commission)
            
        elif choice == 4:
            if signal:
                if self.side == "short" or self.side == "both":
                    self.closePosition(commission)
            else:
                self.closePosition(commission)
            

        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.calc_equity()
            self.portfolioManager.equities.append(self.portfolioManager.update_equity(lastPrice))

    def update_candle_data(self):
        self.lastState = time.time() * 1000
        df = self.dataService.read_data_from_db(self.historyNeeded, self.lastState)
        self.df = df.sort_values(by='timestamp', ascending=True)
        self.df.reset_index(drop=True, inplace=True)
        self.lastCandle = self.df.iloc[-1]

    def mainloop(self):
        print ( f"<----------- Run mainloop on {self.pair} ----------->")
        if self.portfolioManager.get_equity():
            if self.portfolioManager.equity <= 0:
                self.processOrders(4, None, self.settings.constantNumbers["commission"])
                self.portfolioManager.balance = 0
                return
        self.update_candle_data()
        choice, signal = self.orderManager.decider(self.df,
                                                    self.portfolioManager.equity,
                                                    self.portfolioManager.balance,
                                                    self.positionManager.position_average_price(),
                                                    self.positionManager.position_size())
        print ( f"Current choice is:{choice}")
        self.processOrders(choice, signal, self.settings.constantNumbers["commission"])
        self.portfolioManager.calc_poL()

    def check_continue(self):
        print ( f"<----------- Check continue on {self.pair} ----------->")
        self.update_candle_data()
        # print (self.df)
        print ( f"Last candle close: {self.lastCandle['close']}")
        checkContinue = self.positionManager.check_sl_tp(self.lastCandle['close'], self.lastState)
        if not checkContinue :
            print ( f"<----------- Close on SL/TP {self.pair} ----------->")
            self.processOrders(4, None, self.settings.constantNumbers["commission"])
            return