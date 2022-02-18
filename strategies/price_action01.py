from strategies.strategy import Strategy

class PriceAction01(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.marketData = []

    def longEnter(self):
        if self.marketData[-3]['high'] > self.marketData[-4]['high']:
            if self.marketData[-4]['high'] > self.marketData[-5]['high']:
                if self.marketData[-3]['low'] > self.marketData[-4]['low']:
                    if self.marketData[-4]['low'] > self.marketData[-5]['low']:
                        if self.marketData[-2]['close'] > self.marketData[-3]['low']:
                            if self.marketData[-2]['close'] < (self.marketData[-3]['open'] + self.marketData[-3]['close']) / 2:
                                self.decisions['longEnt'] = 1

    def longExit(self):
        if self.marketData[-2]['high'] < self.marketData[-3]['high']:
            if self.marketData[-3]['high'] < self.marketData[-4]['high']:
                if self.marketData[-2]['low'] < self.marketData[-3]['low']:
                    if self.marketData[-3]['low'] < self.marketData[-4]['low']:
                        self.decisions['longExt'] = 1

    def shortEnt(self):
        if self.marketData[-3]['high'] < self.marketData[-4]['high']:
            if self.marketData[-4]['high'] < self.marketData[-5]['high']:
                if self.marketData[-3]['low'] < self.marketData[-4]['low']:
                    if self.marketData[-4]['low'] < self.marketData[-5]['low']:
                        if self.marketData[-2]['close'] < self.marketData[-3]['high']:
                            if self.marketData[-2]['close'] > (self.marketData[-3]['open'] + self.marketData[-3]['close']) / 2:
                                self.decisions['shortEnt'] = 1

    def shortExit(self):
        if self.marketData[-2]['high'] > self.marketData[-3]['high']:
            if self.marketData[-3]['high'] > self.marketData[-4]['high']:
                if self.marketData[-2]['low'] > self.marketData[-3]['low']:
                    if self.marketData[-3]['low'] > self.marketData[-4]['low']:
                        self.decisions['shortExt'] = 1

    def decider(self, marketData):
        self.marketData = marketData
        self.longEnter()
        self.longExit()
        self.shortEnt()
        self.shortExit()
        return self.decisions