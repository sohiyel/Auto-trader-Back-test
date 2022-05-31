from src.strategy import Strategy
from src.signalClass import SignalClass
import pandas as pd
import pandas_ta as ta
from src.logManager import LogService
class OneEMA(Strategy):
    def __init__(self, currentInput, pair, marketData = "", settings="") -> None:
        super().__init__()
        self.pair = pair
        self.marketData = []
        self.df = marketData
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)

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
        if not isinstance(marketData, str):
            self.df["ema"] = ta.ema(self.df["close"], length=self.emaLength)

    def long_enter(self,candle):
        if candle['close'] > candle['ema']:
            self.decisions['longEnt'] = 1
            

    def long_exit(self,candle):
        pass

    def short_enter(self,candle):
        if candle['close'] < candle['ema']:
            self.decisions['shortEnt'] = 1

    def short_exit(self, candle):
        if candle['close'] > candle['ema']:
            self.decisions['shortExt'] = 1

    def decider(self, marketData, timeStamp =""):
        
        self.decisions = {
            'longEnt' : 0,
            'shortEnt' : 0,
            'longExt' : 0,
            'shortExt' : 0,
        }
        if timeStamp:
            candle = self.df.loc[self.df["timestamp"] == timeStamp*1000].iloc[-1]
        else:
            if len(marketData) < self.emaLength:
                self.logger.warning ("-----------Low amount of Data!-----------")
                self.logger.warning("Expected:",str(self.emaLength))
                self.logger.warning("Given:", str(len(marketData)))
                self.logger.warning(marketData.iloc[0]['timestamp'], marketData.iloc[-1]['timestamp'])
                return SignalClass()
            self.df = pd.DataFrame(marketData)
            self.df["ema"] = ta.ema(self.df["close"], length=self.emaLength)
            candle = self.df.iloc[-1]
        self.long_enter(candle)
        self.long_exit(candle)
        self.short_enter(candle)
        self.short_exit(candle)
        sig = SignalClass(pair = self.pair,
                        price = candle["close"],
                        slPercent = self.stopLoss,
                        tpPercent = self.takeProfit,
                        comment= "OneEMA",
                        longEnter = self.decisions["longEnt"],
                        longExit = self.decisions["longExt"],
                        shortEnter = self.decisions["shortEnt"],
                        shortExit = self.decisions["shortExt"])
        return sig