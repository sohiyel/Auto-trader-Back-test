from strategies.strategy import Strategy
import json
from signalClass import SignalClass
import pandas as pd
import pandas_ta as ta

class TwoEMA(Strategy):
    def __init__(self, timeFrame = "default", pair = "default") -> None:
        super().__init__()
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        self.df = ""
        with open("strategies/two_ema.json") as json_data_file:
            strategy = json.load(json_data_file)
            self.params = strategy["params"][0]
            for p in strategy["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    self.params = p
            self.fastEMALength = self.params["inputs"][0]["value"]
            self.slowEMALength = self.params["inputs"][1]["value"]
            self.stopLoss = self.params["exits"]["sl_percent"]
            self.takeProfit = self.params["exits"]["tp_percent"]

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
        self.marketData = marketData
        if len(self.marketData) < self.slowEMALength:
            return SignalClass()
        self.df = pd.DataFrame(marketData)
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