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
from src.simulator import Simulator


class Trader(Simulator):
    def __init__ (self, index, exchange, settings, market = 'futures'):
        self.settings = settings
        self.exchange = exchange
        self.pair = index.pair
        self.side = index.side
        self.startAt = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')
        historyNeeded = index.calc_history_needed()
        self.historyNeeded = int(historyNeeded)
        self.endAt = datetime.fromtimestamp(time.time() - historyNeeded, tz=timezone('utc')).strftime('%Y-%m-%d_%H:%M:%S')
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
