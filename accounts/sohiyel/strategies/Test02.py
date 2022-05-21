from src.strategy import Strategy
from src.signalClass import SignalClass
import pandas as pd
import time
from src.logManager import get_logger
class Test02(Strategy):
    def __init__(self, currentInput, pair, marketData = "", settings = "") -> None:
        super().__init__()
        self.pair = pair
        self.startTime = time.time()
        self.currentTime = 0
        self.logger = get_logger(__name__, settings)

    def long_enter(self):
        longEnters = [1]
        if self.currentTime in longEnters:
            self.decisions['longEnt'] = 1

    def long_exit(self):
        longExits = []
        if self.currentTime in longExits:
            self.decisions['longExt'] = 1

    def short_enter(self):
        shortEnters = [0,3]
        if self.currentTime in shortEnters:
            self.decisions['shortEnt'] = 1

    def short_exit(self):
        shortExits = [4]
        if self.currentTime in shortExits:
            self.decisions['shortExt'] = 1

    def decider(self, marketData, timeStamp =""):
        self.currentTime = int((time.time() - self.startTime)  / 60)
        if len(marketData) < 1:
            self.logger.warning ("-----------Low amount of Data!-----------")
            return SignalClass()
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        self.df = pd.DataFrame(marketData)
        self.long_enter()
        self.long_exit()
        self.short_enter()
        self.short_exit()
        sig = SignalClass(pair = self.pair,
                        price = self.df.iloc[-1]["close"],
                        slPercent = 0,
                        tpPercent = 0,
                        comment= "Test01",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        return sig