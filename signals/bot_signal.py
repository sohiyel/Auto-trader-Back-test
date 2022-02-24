from signalClass import SignalClass
import json
import importlib

class BotSignal():
    def __init__(self, botName, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        self.strategyNames = []
        self.strategies = []
        with open("signals/"+botName+".json") as json_data_file:
            botJson = json.load(json_data_file)
            self.params = botJson["params"][0]
            for p in botJson["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    self.params = p
            for s in botJson["strategies"]:
                self.strategyNames.append(s["strategy"])
        self.slPercent = self.params["exits"]["sl_percent"]
        self.tpPercent = self.params["exits"]["tp_percent"]
        
            
        
        
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        signals = []
        self.strategies = []

        for s in self.strategyNames:
            strategies = importlib.import_module("strategies."+s)
            StrategyClass = getattr(strategies, s)
            self.strategies.append(StrategyClass(self.timeFrame, self.pair))

        for s in self.strategies:
            signals.append(s.decider(self.marketData))

        signal = SignalClass(signals[0].pair,
                            signals[0].type,
                            signals[0].volume,
                            signals[0].price,
                            signals[0].stopLoss,
                            signals[0].takeProfit,
                            self.slPercent,
                            self.tpPercent,
                            '-'.join(s.comment for s in signals),
                            all (s.longEnter == 1 for s in signals),
                            all (s.longExit == 1 for s in signals),
                            all (s.shortEnter == 1 for s in signals),
                            all (s.shortExit == 1 for s in signals))
        # print(self.marketData[-1])
        return signal