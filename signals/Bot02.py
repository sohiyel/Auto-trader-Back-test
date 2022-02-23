from strategies.OneEMA import OneEMA
from strategies.TwoEMA import TwoEMA
from strategies.RSIStrategy import RSIStrategy
from signalClass import SignalClass

class Bot02():
    def __init__(self, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        strategy01 = OneEMA(self.timeFrame, self.pair)
        strategy02 = TwoEMA(self.timeFrame, self.pair)
        strategy03 = RSIStrategy(self.timeFrame, self.pair)
        signal01 = strategy01.decider(self.marketData)
        signal02 = strategy02.decider(self.marketData)
        signal03 = strategy03.decider(self.marketData)
        signal = SignalClass(signal01.pair,
                            signal01.type,
                            signal01.volume,
                            signal01.price,
                            signal01.stopLoss,
                            signal01.takeProfit,
                            signal01.slPercent,
                            signal01.tpPercent,
                            signal01.comment+signal02.comment,
                            signal01.longEnter and signal02.longEnter and signal03.longEnter,
                            signal01.longExit and signal02.longExit and signal03.longExit,
                            signal01.shortEnter and signal02.shortEnter and signal03.shortEnter,
                            signal01.shortExit and signal02.shortExit and signal03.shortExit)
        # print(self.marketData[-1])
        return signal