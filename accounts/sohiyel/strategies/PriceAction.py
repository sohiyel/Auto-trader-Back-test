from src.strategy import Strategy
from src.signalClass import SignalClass

class PriceAction(Strategy):
    def __init__(self, timeFrame = "default", pair = "default") -> None:
        super().__init__()
        self.marketData = []

    def long_enter(self):
        if self.marketData[-3]['high'] > self.marketData[-4]['high']:
            if self.marketData[-4]['high'] > self.marketData[-5]['high']:
                if self.marketData[-3]['low'] > self.marketData[-4]['low']:
                    if self.marketData[-4]['low'] > self.marketData[-5]['low']:
                        if self.marketData[-2]['close'] > self.marketData[-3]['low']:
                            if self.marketData[-2]['close'] < (self.marketData[-3]['open'] + self.marketData[-3]['close']) / 2:
                                self.decisions['longEnt'] = 1

    def long_exit(self):
        if self.marketData[-2]['high'] < self.marketData[-3]['high']:
            if self.marketData[-3]['high'] < self.marketData[-4]['high']:
                if self.marketData[-2]['low'] < self.marketData[-3]['low']:
                    if self.marketData[-3]['low'] < self.marketData[-4]['low']:
                        self.decisions['longExt'] = 1

    def short_enter(self):
        if self.marketData[-3]['high'] < self.marketData[-4]['high']:
            if self.marketData[-4]['high'] < self.marketData[-5]['high']:
                if self.marketData[-3]['low'] < self.marketData[-4]['low']:
                    if self.marketData[-4]['low'] < self.marketData[-5]['low']:
                        if self.marketData[-2]['close'] < self.marketData[-3]['high']:
                            if self.marketData[-2]['close'] > (self.marketData[-3]['open'] + self.marketData[-3]['close']) / 2:
                                self.decisions['shortEnt'] = 1

    def short_exit(self):
        if self.marketData[-2]['high'] > self.marketData[-3]['high']:
            if self.marketData[-3]['high'] > self.marketData[-4]['high']:
                if self.marketData[-2]['low'] > self.marketData[-3]['low']:
                    if self.marketData[-3]['low'] > self.marketData[-4]['low']:
                        self.decisions['shortExt'] = 1

    def decider(self, marketData):
        self.marketData = marketData
        if len(self.marketData) < 5:
            return SignalClass()
        self.long_enter()
        self.long_exit()
        self.short_enter()
        self.short_exit()
        sig = SignalClass(price = self.marketData[-1]["close"], longEnter = self.decisions["longEnt"], longExit = self.decisions["longExt"], shortEnter = self.decisions["shortEnt"], shortExit = self.decisions["shortExt"])
        return sig