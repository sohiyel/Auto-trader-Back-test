from logging import currentframe
import pandas as pd
from src.positionManager import PositionManager
from src.orderManager import OrderManager
from src.data import DataService
from src.portfolioManager import PortfolioManager
from src.utility import Utility
from datetime import datetime
from pytz import timezone
import time
from src.simulator import Simulator
from src.logManager import LogService

class Trader(Simulator):
    def __init__ (self, index, settings, market = 'futures'):
        self.settings = settings
        self.exchange = settings.exchange_service
        self.pair = index.pair
        self.timeFrame = Utility.unify_timeframe(index.timeFrame, settings.exchange)
        self.side = index.side
        self.startAt = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')
        historyNeeded = index.calc_history_needed()
        self.historyNeeded = int(historyNeeded)
        self.endAt = datetime.fromtimestamp(time.time() - historyNeeded, tz=timezone('utc')).strftime('%Y-%m-%d_%H:%M:%S')
        self.dataService = DataService(market, index.pair, self.timeFrame, self.startAt, self.endAt, historyNeeded, settings)
        self.startAtTS = self.dataService.startAtTs
        self.endAtTS = self.dataService.endAtTs
        self.lastState = self.dataService.startAtTs
        self.strategyName = index.strategyName
        self.botName = index.botName
        self.portfolioManager = PortfolioManager(index.pair,1, settings)
        self.initialCapital = self.portfolioManager.get_equity()
        self.orderManager = OrderManager(self.initialCapital, index.strategyName, index.botName, index.inputs, index.pair, settings)
        self.lastCandle = ""
        self.volume = index.amount
        self.ratioAmount = index.ratioAmount
        self.leverage = index.leverage
        self.positionManager = PositionManager(self.portfolioManager.initialCapital, self.pair, self.volume, self.ratioAmount, self.timeFrame, self.strategyName, self.botName, self.leverage,settings)
        self.positionManager.sync_positions()
        self.currentInput = index
        self.df = ""
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)

    def update_candle_data(self):
        self.lastState = time.time() * 1000
        df = self.dataService.read_data_from_db(self.historyNeeded, self.lastState)
        self.df = df.sort_values(by='timestamp', ascending=True)
        self.df.reset_index(drop=True, inplace=True)
        self.lastCandle = self.df.iloc[-1]

    def mainloop(self):
        self.logger.info ( f"<----------- Run mainloop on {self.pair} ----------->")
        if self.portfolioManager.get_equity():
            if self.portfolioManager.equity <= 0:
                self.processOrders(4, None, self.settings.constantNumbers["commission"])
                self.portfolioManager.balance = 0
                return
        try:
            self.update_candle_data()
        except:
            self.logger.error("Cannot update candle data!")
        choice, signal = self.orderManager.decider(self.df,
                                                    self.portfolioManager.equity,
                                                    self.portfolioManager.balance,
                                                    self.positionManager.position_average_price(),
                                                    self.positionManager.position_size())
        self.logger.info ( f"Current choice is:{choice}")
        try:
            self.processOrders(choice, signal, self.settings.constantNumbers["commission"])
        except Exception as e:
            self.logger.error("Cannot process this signal!" + str(e))
        self.portfolioManager.calc_poL()
