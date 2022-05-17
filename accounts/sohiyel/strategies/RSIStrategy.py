from src.strategy import Strategy
from src.signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from src.logManager import get_logger

class RSIStrategy(Strategy):
    def __init__(self, currentInput, pair, marketData = "",settings="") -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        self.logger = get_logger(__name__, settings)
        self.df = marketData
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
        if not isinstance(marketData, str):
            self.df["rsiLength"] = ta.ema(self.df["close"], length=self.rsiLength)
            self.df["rsiMidLine"] = ta.ema(self.df["close"], length=self.rsiMidLine)

    def long_enter(self, candle):
        if candle.iloc[-1]["rsiLength"] > candle.iloc[-1]["rsiMidLine"]:
            self.decisions['longEnt'] = 1
            

    def long_exit(self, candle):
        pass

    def short_enter(self,candle):
        if candle.iloc[-1]["rsiLength"] < candle.iloc[-1]["rsiMidLine"]:
            self.decisions['shortEnt'] = 1

    def short_exit(self, candle):
        if candle.iloc[-1]["rsiLength"] > candle.iloc[-1]["rsiMidLine"]:
            self.decisions['shortExt'] = 1

    def decider(self, marketData, timeStamp =""):
        if len(marketData) < self.rsiLength:
            self.logger.warning ("-----------Low amount of Data!-----------")
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
            self.df["rsiLength"] = ta.ema(self.df["close"], length=self.rsiLength)
            self.df["rsiMidLine"] = ta.ema(self.df["close"], length=self.rsiMidLine)
            candle = self.df.loc[self.df["timestamp"] == self.df.iloc[-1]["timestamp"]]
        self.long_enter(candle)
        self.long_exit(candle)
        self.short_enter(candle)
        self.short_exit(candle)
        sig = SignalClass(pair = self.pair,
                        price = candle.iloc[-1]["close"],
                        slPercent = self.stopLoss,
                        tpPercent = self.takeProfit,
                        comment = "RSI",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        return sig