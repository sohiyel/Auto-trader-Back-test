from strategies.strategy import Strategy
import json
from signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from itertools import chain

class RSIStrategy(Strategy):
    def __init__(self, currentInput, pair) -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        
        self.df = ""
        if type(currentInput[0]) == tuple:
            for i in currentInput:
                if i[0].strategy == "RSIStrategy":
                    self.rsiLength = next((x.value for x in i if x.name == "len"), None)
                    self.rsiMidLine = next((x.value for x in i if x.name == "mid_line"), None)
                    self.stopLoss = next((x.value for x in i if x.name == "sl_percent"), 0.3)
                    self.takeProfit = next((x.value for x in i if x.name == "tp_percent"), 0.5)
                    break
        else:
            self.rsiLength = next((x.value for x in currentInput if x.name == "len"), None)
            self.rsiMidLine = next((x.value for x in currentInput if x.name == "mid_line"), None)
            self.stopLoss = next((x.value for x in currentInput if x.name == "sl_percent"), 0.3)
            self.takeProfit = next((x.value for x in currentInput if x.name == "tp_percent"), 0.5)
        

    def long_enter(self):
        if self.rsi.iloc[-1] > self.rsiMidLine:
            self.decisions['longEnt'] = 1
            

    def long_exit(self):
        pass

    def short_enter(self):
        if self.rsi.iloc[-1] < self.rsiMidLine:
            self.decisions['shortEnt'] = 1

    def short_exit(self):
        if self.rsi.iloc[-1] > self.rsiMidLine:
            self.decisions['shortExt'] = 1

    def decider(self, marketData):
        if len(marketData) < self.rsiLength:
            return SignalClass()

        self.marketData = marketData
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        self.df = ""
        self.df = pd.DataFrame(self.marketData)
        self.rsi = ta.rsi(self.df["close"], length= self.rsiLength)
        self.long_enter()
        self.long_exit()
        self.short_enter()
        self.short_exit()
        sig = SignalClass(pair = self.pair,
                        price = self.df.iloc[-1]["close"],
                        slPercent = self.stopLoss,
                        tpPercent = self.takeProfit,
                        comment = "RSI",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        # print(sig)
        return sig