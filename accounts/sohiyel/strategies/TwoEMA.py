from src.strategy import Strategy
import json
from src.signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from itertools import chain
class TwoEMA(Strategy):
    def __init__(self, currentInput, pair, marketData = "") -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        self.df = marketData
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
        if not isinstance(marketData, str):
            self.df["fastEMA"] = ta.ema(self.df["close"], length=self.fastEMALength)
            self.df["slowEMA"] = ta.ema(self.df["close"], length=self.slowEMALength)

    def long_enter(self, candle):
        if candle.iloc[-1]["fastEMA"] > candle.iloc[-1]["slowEMA"]:
            self.decisions['longEnt'] = 1
            

    def long_exit(self, candle):
        pass

    def short_enter(self, candle):
        if candle.iloc[-1]["fastEMA"] < candle.iloc[-1]["slowEMA"]:
            self.decisions['shortEnt'] = 1

    def short_exit(self, candle):
        if candle.iloc[-1]["fastEMA"] > candle.iloc[-1]["slowEMA"]:
            self.decisions['shortExt'] = 1

    def decider(self, marketData, timeStamp =""):
        if len(marketData) < self.slowEMALength:
            print ("-----------Low amount of Data!-----------")
            return SignalClass()
        
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        if timeStamp:
            candle = self.df.loc[self.df["timestamp"] == timeStamp*1000]
        else:
            self.marketData = marketData
            self.df = pd.DataFrame(self.marketData)
            self.df["fastEMA"] = ta.ema(self.df["close"], length=self.fastEMALength)
            self.df["slowEMA"] = ta.ema(self.df["close"], length=self.slowEMALength)
            candle = self.df.loc[self.df["timestamp"] == self.df.iloc[-1]["timestamp"]]
        self.long_enter(candle)
        self.long_exit(candle)
        self.short_enter(candle)
        self.short_exit(candle)
        sig = SignalClass(pair = self.pair,
                        price = candle.iloc[-1]["close"],
                        slPercent = self.stopLoss,
                        tpPercent = self.takeProfit,
                        comment = "TwoEMA",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        # print(sig)
        return sig