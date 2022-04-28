from src.strategy import Strategy
import json
from src.signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from itertools import chain

class OneEMA(Strategy):
    def __init__(self, currentInput, pair) -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        self.df = ""
        # print(currentInput)
        if type(currentInput[0]) == tuple:
            for i in currentInput:
                if i[0].strategy == "OneEMA":
                    self.emaLength = next((x.value for x in i if x.name == "len"), None)
                    self.stopLoss = next((x.value for x in i if x.name == "sl_percent"), 0.3)
                    self.takeProfit = next((x.value for x in i if x.name == "tp_percent"), 0.5)
                    break
        else:
            self.emaLength = next((x.value for x in currentInput if x.name == "len"), None)
            self.stopLoss = next((x.value for x in currentInput if x.name == "sl_percent"), 0.3)
            self.takeProfit = next((x.value for x in currentInput if x.name == "tp_percent"), 0.5)

    def long_enter(self):
        if self.df.iloc[-1]['close'] > self.ema.iloc[-1]:
            self.decisions['longEnt'] = 1
            

    def long_exit(self):
        pass

    def short_enter(self):
        if self.df.iloc[-1]['close'] < self.ema.iloc[-1]:
            self.decisions['shortEnt'] = 1

    def short_exit(self):
        if self.df.iloc[-1]['close'] > self.ema.iloc[-1]:
            self.decisions['shortExt'] = 1

    def decider(self, marketData):
        if len(marketData) < self.emaLength:
            print ("-----------Low amount of Data!-----------")
            return SignalClass()
        
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        self.df = pd.DataFrame(marketData)
        self.ema = ta.ema(self.df["close"], length=self.emaLength)
        self.long_enter()
        self.long_exit()
        self.short_enter()
        self.short_exit()
        sig = SignalClass(pair = self.pair,
                        price = self.df.iloc[-1]["close"],
                        slPercent = self.stopLoss,
                        tpPercent = self.takeProfit,
                        comment= "OneEMA",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        # print(sig)
        return sig