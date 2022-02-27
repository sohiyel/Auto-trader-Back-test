from strategies.strategy import Strategy
import json
from signalClass import SignalClass
import pandas as pd
import pandas_ta as ta

class RSIStrategy(Strategy):
    def __init__(self, currentInput) -> None:
        super().__init__()
        self.marketData = []
        self.df = ""
        self.rsiLength = next((x.value for x in currentInput if x.name == "len"), None)
        self.rsiMidLine = next((x.value for x in currentInput if x.name == "mid_line"), None)
        self.stopLoss = next((x.value for x in currentInput if x.name == "sl_percent"), 0.3)
        self.takeProfit = next((x.value for x in currentInput if x.name == "tp_percent"), 0.5)

    def longEnter(self):
        if self.rsi.iloc[-1] > self.rsiMidLine:
            self.decisions['longEnt'] = 1
            

    def longExit(self):
        pass

    def shortEnt(self):
        if self.rsi.iloc[-1] < self.rsiMidLine:
            self.decisions['shortEnt'] = 1

    def shortExit(self):
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
        self.longEnter()
        self.longExit()
        self.shortEnt()
        self.shortExit()
        sig = SignalClass(pair = "BTC-USDT",
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