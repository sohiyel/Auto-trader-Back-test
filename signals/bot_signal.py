from signalClass import SignalClass
import json
import importlib

class BotSignal():
    def __init__(self, botName, currentInput, timeFrame="default", pair="default") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        self.strategyNames = []
        self.strategies = []
        json_data_file = open("signals/"+botName+".json")
        botJson = json.load(json_data_file)
        
        for s in botJson["strategies"]:
            self.strategyNames.append(s["strategy"])
        
        for s in self.strategyNames:
            strategies = importlib.import_module("strategies."+s)
            StrategyClass = getattr(strategies, s)
            self.strategies.append(StrategyClass(currentInput, self.pair))
        json_data_file.close()
        
        
    def decider(self, marketData):
        self.marketData = marketData
        signals = []

        for s in self.strategies:
            signals.append(s.decider(self.marketData))

        signal = SignalClass(signals[0].pair,
                            signals[0].side,
                            signals[0].volume,
                            signals[0].price,
                            signals[0].stopLoss,
                            signals[0].takeProfit,
                            signals[0].slPercent,
                            signals[0].tpPercent,
                            '-'.join(s.comment for s in signals),
                            all (s.longEnter == 1 for s in signals),
                            all (s.longExit == 1 for s in signals),
                            all (s.shortEnter == 1 for s in signals),
                            all (s.shortExit == 1 for s in signals))
        # print(self.marketData[-1])
        return signal