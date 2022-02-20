from strategies.strategy import Strategy
import json

class OneEMA(Strategy):
    def __init__(self, timeFrame = "default", pair = "default") -> None:
        super().__init__()
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        with open("one_ema.json") as json_data_file:
            strategy = json.load(json_data_file)
            self.params = strategy["params"][0]
            for p in strategy["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    self.params = p

    def longEnter(self):
        if self.marketData[-1]['close'] > self.marketData[-1]['EMA_'+str(self.params["value"])]:
            self.decisions['longEnt'] = 1
            

    def longExit(self):
        pass

    def shortEnt(self):
        if self.marketData[-1]['close'] < self.marketData[-1]['EMA_'+str(self.params["value"])]:
            self.decisions['shortEnt'] = 1

    def shortExit(self):
        if self.marketData[-1]['close'] > self.marketData[-1]['EMA_'+str(self.params["value"])]:
            self.decisions['shortExt'] = 1

    def decider(self, marketData):
        self.marketData = marketData
        self.longEnter()
        self.longExit()
        self.shortEnt()
        self.shortExit()
        return self.decisions