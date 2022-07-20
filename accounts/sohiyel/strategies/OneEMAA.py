from src.strategy import Strategy
from src.signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from src.logManager import LogService

class OneEMAA(Strategy):
    def __init__(self, currentInput, pair, marketData = "", settings="") -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        self.df = marketData
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        pts = {'pair': self.pair, 'timeFrame': 'NaN', 'strategyName': 'OneEMA'}
        self.logService.set_pts_formatter(pts)
        self.logger.debug("Initializing OneEMAA...")
        if type(currentInput[0]) == tuple:
            self.logger.debug("OneEMAA inputs are tuple")
            for i in currentInput:
                if i[0].strategy == "OneEMA":
                    self.hlc3 = next((x.value for x in i if x.name == "source"), None)
                    self.displacement = next((-1 * x.value for x in i if x.name == "displacement"), None)
                    self.emaLength = next((x.value for x in i if x.name == "len"), None)
                    self.stopLoss = next((x.value for x in i if x.name == "sl_percent"), 0.3)
                    self.takeProfit = next((x.value for x in i if x.name == "tp_percent"), 0.5)
                    break
        else:
            self.logger.debug("OneEMAA inputs are not tuple")
            self.hlc3 = next((x.value for x in currentInput if x.name == "source"), None)
            self.logger.debug(f"hlc3 is {self.hlc3}")
            self.displacement = next((-1 * x.value for x in currentInput if x.name == "displacement"), None)
            self.logger.debug(f"Displacement is {self.displacement}")
            self.emaLength = next((x.value for x in currentInput if x.name == "len"), None)
            self.logger.debug(f"emaLength is {self.emaLength}")
            self.stopLoss = next((x.value for x in currentInput if x.name == "sl_percent"), 0.3)
            self.logger.debug(f"stopLoss is {self.stopLoss}")
            self.takeProfit = next((x.value for x in currentInput if x.name == "tp_percent"), 0.5)
            self.logger.debug(f"TakeProfit is {self.takeProfit}")
        if not isinstance(marketData, str):
            self.logger.debug("Market data have provided")
            if self.hlc3:
                self.df["hlc3"] = (self.df["high"] + self.df["low"] + self.df["close"]) / 3
                self.df["ema"] = ta.ema(self.df["hlc3"], length=self.emaLength)
            else:
                self.df["ema"] = ta.ema(self.df["close"], length=self.emaLength)

    def long_enter(self,candle):
        if candle.iloc[-1]['close'] > candle.iloc[self.displacement]['ema']:
            self.decisions['longEnt'] = 1
            

    def long_exit(self,candle):
        pass

    def short_enter(self,candle):
        if candle.iloc[-1]['close'] < candle.iloc[self.displacement]['ema']:
            self.decisions['shortEnt'] = 1

    def short_exit(self, candle):
        if candle.iloc[-1]['close'] > candle.iloc[self.displacement]['ema']:
            self.decisions['shortExt'] = 1

    def decider(self, marketData, timeStamp =""):
        
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        if timeStamp:
            candle = self.df.loc[self.df["timestamp"] <= timeStamp*1000]
        else:
            if len(marketData) < self.emaLength:
                self.logger.warning ("-----------Low amount of Data!-----------")
                return SignalClass()
            self.df = pd.DataFrame(marketData)
            if self.hlc3:
                self.df["hlc3"] = (self.df["high"] + self.df["low"] + self.df["close"]) / 3
                self.df["ema"] = ta.ema(self.df["hlc3"], length=self.emaLength)
            else:
                self.df["ema"] = ta.ema(self.df["close"], length=self.emaLength)
            candle = self.df
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
        return sig