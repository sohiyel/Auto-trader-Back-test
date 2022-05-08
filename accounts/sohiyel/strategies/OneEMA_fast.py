from src.strategy import Strategy
import json
from src.signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from itertools import chain

class OneEMA_fast(Strategy):
    def __init__(self, currentInput, pair, marketData="") -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        self.df = marketData
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
        self.df["ema"] = ta.ema(self.df["close"], length=self.emaLength)

    def long_enter(self,candle):
        if candle.iloc[-1]['close'] > candle.iloc[-1]['ema']:
            self.decisions['longEnt'] = 1
            

    def long_exit(self,candle):
        pass

    def short_enter(self,candle):
        if candle.iloc[-1]['close'] < candle.iloc[-1]['ema']:
            self.decisions['shortEnt'] = 1

    def short_exit(self, candle):
        if candle.iloc[-1]['close'] > candle.iloc[-1]['ema']:
            self.decisions['shortExt'] = 1

    def decider(self, marketData, timeStamp = ""):
        # print(self.df.iloc[0])
        # print("timeStamp:"+ str(timeStamp))
        candle = self.df.loc[self.df["timestamp"] == timeStamp*1000]
        # print(candle)
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        self.long_enter(candle)
        self.long_exit(candle)
        self.short_enter(candle)
        self.short_exit(candle)
        sig = SignalClass(pair = self.pair,
                        price = candle.iloc[-1]["close"],
                        slPercent = self.stopLoss,
                        tpPercent = self.takeProfit,
                        comment= "OneEMA",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        # print(sig)
        return sig