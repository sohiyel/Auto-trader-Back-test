from src.signalClass import SignalClass
import json
import importlib
from os import path
from src.logManager import get_logger
class BotSignal():
    def __init__(self, botName, currentInput, timeFrame="default", pair="default", settings="", marketData="") -> None:
        self.lastSignal = 0
        self.marketData = []
        self.timeFrame = timeFrame
        self.pair = pair
        self.strategyNames = []
        self.strategies = []
        botFile = botName + ".json"
        self.logger = get_logger(__name__, settings)
        try:
            json_data_file = open( path.join(settings.SIGNALS_DIR, botFile))
            botJson = json.load(json_data_file)
        except:
            self.logger(f"Cannot load {botFile}")
        
        for s in botJson["strategies"]:
            self.strategyNames.append(s["strategy"])
        
        for s in self.strategyNames:
            try:
                strategies = importlib.import_module(settings.STRATEGIES_MODULE_PATH+s)
                StrategyClass = getattr(strategies, s)
                self.strategies.append(StrategyClass(currentInput, self.pair, marketData, settings))
            except:
                self.logger.error(f"Cannot import this strategy{s}")
        try:
            self.andEnter = botJson["and_or_strategies"]["enter_strategies_and"]
            self.andExit = botJson["and_or_strategies"]["exit_strategies_and"]
        except:
            self.logger.error("This strategy does not have add_or_strategies!")
        json_data_file.close()
        
    
    def get_final_decision(self, signals):
        decision = {
            "longEnter": False,
            "longExit": False,
            "shortEnter": False,
            "shortExit": False
        }
        if self.andEnter:
            if all (s.longEnter == 1 for s in signals):
                decision["longEnter"] = True
            else:
                decision["longEnter"] = False
            if all (s.shortEnter == 1 for s in signals):
                decision["shortEnter"] = True
            else:
                decision["shortEnter"] = False
        else:
            for s in signals:
                if s.longEnter:
                    decision["longEnter"] = True
                if s.shortEnter:
                    decision["shortEnter"] = True
        if self.andExit:
            if all (s.longExit == 1 for s in signals):
                decision["longExit"] = True
            else:
                decision["longExit"] = False
            if all (s.shortExit == 1 for s in signals):
                decision["shortExit"] = True
            else:
                decision["shortExit"] = False
        else:
            for s in signals:
                if s.longExit:
                    decision["longExit"] = True
                if s.shortExit:
                    decision["shortExit"] = True
        return decision

    def decider(self, marketData="", timestamp=""):
        self.marketData = marketData
        signals = []

        for s in self.strategies:
            signals.append(s.decider(self.marketData, timestamp))
        try:
            decision = self.get_final_decision(signals)
        except:
            self.logger.error("Cannot get final decision!")
        signal = SignalClass(signals[0].pair,
                            signals[0].side,
                            signals[0].volume,
                            signals[0].price,
                            signals[0].stopLoss,
                            signals[0].takeProfit,
                            signals[0].slPercent,
                            signals[0].tpPercent,
                            '-'.join(s.comment for s in signals),
                            decision["longEnter"],
                            decision["longExit"],
                            decision["shortEnter"],
                            decision["shortExit"])
        return signal