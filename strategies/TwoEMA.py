from strategies.strategy import Strategy
import json
from signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from itertools import chain
class TwoEMA(Strategy):
    def __init__(self, currentInput, pair) -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        self.df = ""
        if type(currentInput[0]) == tuple:
            for i in currentInput:
                if i[0].strategy == "TwoEMA":
                    self.fastEMALength = next((x.value for x in i if x.name == "fast_len"), None)
                    self.slowEMALength = next((x.value for x in i if x.name == "slow_len"), None)
                    self.stopLoss = next((x.value for x in i if x.name == "sl_percent"), 0.3)
                    self.takeProfit = next((x.value for x in i if x.name == "tp_percent"), 0.5)
                    break
        else:
            self.fastEMALength = next((x.value for x in currentInput if x.name == "fast_len"), None)
            self.slowEMALength = next((x.value for x in currentInput if x.name == "slow_len"), None)
            self.stopLoss = next((x.value for x in currentInput if x.name == "sl_percent"), 0.3)
            self.takeProfit = next((x.value for x in currentInput if x.name == "tp_percent"), 0.5)

    def longEnter(self):
        if self.fastEMA.iloc[-1] > self.slowEMA.iloc[-1]:
            self.decisions['longEnt'] = 1
            

    def longExit(self):
        pass

    def shortEnt(self):
        if self.fastEMA.iloc[-1] < self.slowEMA.iloc[-1]:
            self.decisions['shortEnt'] = 1

    def shortExit(self):
        if self.fastEMA.iloc[-1] > self.slowEMA.iloc[-1]:
            self.decisions['shortExt'] = 1

    def decider(self, marketData):
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        if len(marketData) < self.slowEMALength:
            return SignalClass()
        self.marketData = marketData
        self.df = pd.DataFrame(self.marketData)
        self.fastEMA = ta.ema(self.df["close"], length=self.fastEMALength)
        self.slowEMA = ta.ema(self.df["close"], length=self.slowEMALength)
        self.longEnter()
        self.longExit()
        self.shortEnt()
        self.shortExit()
        sig = SignalClass(pair = self.pair,
                        price = self.df.iloc[-1]["close"],
                        slPercent = self.stopLoss,
                        tpPercent = self.takeProfit,
                        comment = "TwoEMA",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        # print(sig)
        return sig