from strategies.OneEMA import OneEMA
from strategies.TwoEMA import TwoEMA
from signalClass import SignalClass
import json

class Bot01():
    def __init__(self, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        with open("signals/bot1.json") as json_data_file:
            bot01 = json.load(json_data_file)
            self.params = bot01["params"][0]
            for p in bot01["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    self.params = p
        self.slPercent = self.params["exits"]["sl_percent"]
        self.tpPercent = self.params["exits"]["tp_percent"]
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        strategy01 = OneEMA(self.timeFrame, self.pair)
        strategy02 = TwoEMA(self.timeFrame, self.pair)
        signal01 = strategy01.decider(self.marketData)
        signal02 = strategy02.decider(self.marketData)
        signal = SignalClass(signal01.pair,
                            signal01.type,
                            signal01.volume,
                            signal01.price,
                            signal01.stopLoss,
                            signal01.takeProfit,
                            self.slPercent,
                            self.tpPercent,
                            signal01.comment+signal02.comment,
                            signal01.longEnter and signal02.longEnter,
                            signal01.longExit and signal02.longExit,
                            signal01.shortEnter and signal02.shortEnter,
                            signal01.shortExit and signal02.shortExit)
        # print(self.marketData[-1])
        return signal