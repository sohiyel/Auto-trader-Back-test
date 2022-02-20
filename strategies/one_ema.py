from strategies.strategy import Strategy
import json
from signalClass import SignalClass
import pandas as pd
import pandas_ta as ta

class OneEMAStrategy(Strategy):
    def __init__(self, timeFrame = "default", pair = "default") -> None:
        super().__init__()
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        self.df = ""
        with open("strategies/one_ema.json") as json_data_file:
            strategy = json.load(json_data_file)
            self.params = strategy["params"][0]
            for p in strategy["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    self.params = p
            self.emaLength = self.params["inputs"][0]["value"]

    def longEnter(self):
        if self.df.iloc[-1]['close'] > self.ema.iloc[-1]:
            self.decisions['longEnt'] = 1
            

    def longExit(self):
        pass

    def shortEnt(self):
        if self.df.iloc[-1]['close'] < self.ema.iloc[-1]:
            self.decisions['shortEnt'] = 1

    def shortExit(self):
        if self.df.iloc[-1]['close'] > self.ema.iloc[-1]:
            self.decisions['shortExt'] = 1

    def decider(self, marketData):
        self.marketData = marketData
        self.df = pd.DataFrame(marketData)
        self.ema = ta.ema(self.df["close"], length=self.emaLength)
        self.longEnter()
        self.longExit()
        self.shortEnt()
        self.shortExit()
        sig = SignalClass(self.pair, price = self.df.iloc[-1]["close"], longEnter = self.decisions["longEnt"], longExit = self.decisions["longExt"], shortEnter = self.decisions["shortEnt"], shortExit = self.decisions["shortExt"])
        # print(sig)
        return sig