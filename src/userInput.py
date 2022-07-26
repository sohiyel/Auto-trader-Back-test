import json
from src.paramInput import ParamInput
import itertools
import numpy as np
from random import shuffle
import time
from src.utility import Utility
from os import path
from src.logManager import LogService

class UserInput():
    def __init__(self, pair, timeFrame, strategyName, botName, side = "both", leverage = 1, amount = 1 , ratioAmount = 0, optimization = False, randomInput = False, settings="") -> None:
        self.settings = settings
        self.pair = pair
        self.timeFrame = Utility.unify_timeframe(timeFrame, settings.exchange)
        self.strategyName = strategyName
        self.botName = botName
        self.side = side
        self.leverage = leverage
        self.amount = amount
        self.ratioAmount = ratioAmount
        self.optimization = optimization
        self.step = 0
        self.inputs = []
        self.randomInput = randomInput
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        pts = {'pair': self.pair, 'timeFrame': self.timeFrame, 'strategyName': self.strategyName}
        self.logService.set_pts_formatter(pts)

    def __eq__(self, other) -> bool:
        if self.pair == other.pair and self.timeFrame == other.timeFrame and\
            self.strategyName == other.strategyName and self.botName == other.botName and\
                self.leverage == other.leverage and self.amount == other.amount:
                return True
        return False

    def find_inputs(self):
        if self.botName:
            try:
                self.inputs= self.get_bot_inputs()
            except:
                self.logger.error("Cannot get bot inputs!")
        else:
            try:
                self.inputs = self.get_strategy_inputs(self.strategyName)
            except:
                self.logger.error("Cannot get strategy input!")
        if self.randomInput:
            shuffle(self.inputs)


    def get_strategy_inputs(self, strategyName):
        strategyFileName = strategyName + ".json"
        try:
            json_data_file = open(path.join(self.settings.STRATEGIES_DIR , strategyFileName))
            jsonFile = json.load(json_data_file)
        except:
            self.logger.error(f"Cannot open {strategyFileName}!")
            raise FileNotFoundError(f"Cannot open {strategyFileName}!")
        inputs = []
        if self.optimization:
            try:
                for i in jsonFile["optimization"]["inputs"]:
                    pi = ParamInput(i["name"], i["value"], i["strategy"], i["historyNeeded"], i["minValue"], i["maxValue"], i["step"], i["optimization"])
                    if pi.optimization:
                        strategyInputs = []
                        for i in np.arange(pi.minValue, pi.maxValue+1, pi.step):
                            strategyInputs.append(ParamInput(pi.name, i, pi.strategy, pi.historyNeeded , pi.minValue, pi.maxValue, pi.step, pi.optimization))
                        inputs.append(strategyInputs)
                    else:
                        inputs.append([pi])
            except:
                self.logger.error(f"Insufficient parameters in {strategyFileName}")
                raise NotImplementedError(f"Insufficient parameters in {strategyFileName}")
        else:
            try:    
                if len(jsonFile["params"]) > 0:
                    params = jsonFile["params"][0]
                    for p in jsonFile["params"]:
                        if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                            params = p
                    for i in params["inputs"]:
                        pi = ParamInput(i["name"], i["value"],i["strategy"], i["historyNeeded"])
                        inputs.append([pi])
                else:
                    params = ""
                    inputs = []
            except:
                self.logger.error(f"Insufficient parameters in {strategyFileName}")
                raise NotImplementedError(f"Insufficient parameters in {strategyFileName}")
        
        json_data_file.close()
        return list( itertools.product( *inputs ) )

    def get_bot_inputs(self):
        botFileName = self.botName + ".json"
        try:
            json_data_file = open(path.join(self.settings.SIGNALS_DIR , botFileName))
            jsonFile = json.load(json_data_file)
        except:
            self.logger.error(f"Cannot load {botFileName}!")
            raise FileNotFoundError(f"Cannot load {botFileName}!")
        inputs = []
        if self.optimization:
            try:
                for i in jsonFile["optimization"]["inputs"]:
                    pi = ParamInput(i["name"], i["value"], i["strategy"], i["historyNeeded"], i["minValue"], i["maxValue"], i["step"], i["optimization"])
                    if pi.optimization:
                        strategyInputs = []
                        for i in np.arange(pi.minValue, pi.maxValue+1, pi.step):
                            strategyInputs.append(ParamInput(pi.name, i, pi.strategy, pi.historyNeeded, pi.minValue, pi.maxValue, pi.step, pi.optimization))
                        inputs.append(strategyInputs)
                    else:
                        inputs.append([pi])
            except:
                self.logger.error(f"Insufficient parameters in {botFileName}")
                raise NotImplementedError(f"Insufficient parameters in {botFileName}")
        else:
            try:    
                params = jsonFile["params"][0]
                for p in jsonFile["params"]:
                    if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                        params = p
                for i in params["inputs"]:
                    pi = ParamInput(i["name"], i["value"],i["strategy"], i["historyNeeded"])
                    inputs.append([pi])
            except:
                self.logger.error(f"Insufficient parameters in {botFileName}")
                raise NotImplementedError(f"Insufficient parameters in {botFileName}")
        
        json_data_file.close()
        return list( itertools.product( *inputs ) )

    def get_current_input(self):
        return self.inputs[self.step]

    def get_strategy_names(self):
        strategyNames = []
        botFileName = self.botName + ".json"
        try:
            json_data_file = open(path.join(self.settings.SIGNALS_DIR , botFileName))
            jsonFile = json.load(json_data_file)
        except:
            self.logger.error(f"Cannot load {botFileName}!")
            raise FileNotFoundError(f"Cannot load {botFileName}!")
        for s in jsonFile["strategies"]:
            strategyNames.append(s["strategy"])
        json_data_file.close()
        return strategyNames

    def get_input_names(self):
        names = []
        if self.botName:
            botFileName = self.botName + ".json"
            try:
                with open(path.join(self.settings.SIGNALS_DIR , botFileName), 'r+') as json_data_file:
                    jsonFile = json.load(json_data_file)
            except:
                self.logger.error(f"Cannot load {botFileName}")
                raise FileNotFoundError(f"Cannot load {botFileName}")
        else:
            strategyFileName = self.strategyName + ".json"
            try:
                with open(path.join(self.settings.STRATEGIES_DIR , strategyFileName), 'r+') as json_data_file:
                    jsonFile = json.load(json_data_file)
            except:
                self.logger.error(f"Cannot open {strategyFileName}")
                raise FileNotFoundError(f"Cannot open {strategyFileName}")
        
        try:
            params = jsonFile["params"][0]
            for i in params["inputs"]:
                names.append( (i["name"],i["strategy"],i["historyNeeded"]) )
        except:
            self.logger.error(f"Insufficient parameters in {strategyFileName}")
        
        json_data_file.close()
        return names

    def write_optimized_values(self, report):
        inputNames = []
        if self.botName:
            botFileName = self.botName + ".json"
            try:
                with open(path.join(self.settings.SIGNALS_DIR , botFileName), 'r+') as json_data_file:
                    jsonFile = json.load(json_data_file)
            except:
                self.logger.error(f"Cannot load {botFileName}!")
        else:
            strategyFileName = self.strategyName + ".json"
            try:
                with open(path.join(self.settings.STRATEGIES_DIR , strategyFileName), 'r+') as json_data_file:
                    jsonFile = json.load(json_data_file)
            except:
                self.logger.error(f"Cannot load {strategyFileName}!")
        inputNames = self.get_input_names()

        paramExist = False
        try:
            for idx,param in enumerate(jsonFile["params"]):
                if param["time_frame"] == self.timeFrame and param["pair"] == self.pair:
                    paramExist = True
                    for n in inputNames:
                        value = float(report[n[1] + "_" + n[0]])
                        inputExist = False
                        for i in range(len(jsonFile["params"][idx]["inputs"])):
                            if jsonFile["params"][idx]["inputs"][i]["name"] == n[0] and jsonFile["params"][idx]["inputs"][i]["strategy"] == n[1]:
                                jsonFile["params"][idx]["inputs"][i]["value"] = value
                                inputExist = True
                                break
                        if not inputExist:
                            newInput = ParamInput(n[0], value, n[1],n[2])
                            jsonFile["params"][idx]["inputs"].append(newInput.to_dict())
                    jsonFile["params"][idx]["optimization_date"] = time.strftime("%Y-%m-%d_%H:%M:%S")
        except:
            self.logger.error(f"Insufficient parameters in {strategyFileName}")

        if not paramExist:
            newParam = {}
            newParam["time_frame"] = self.timeFrame
            newParam["pair"] = self.pair
            newParam["optimization_date"] = time.strftime("%Y-%m-%d_%H:%M:%S")
            newParam["inputs"] = []
            for n in inputNames:
                value = float(report[n[1] + "_" + n[0]])
                newParam["inputs"].append(ParamInput(n[0], value, n[1],n[2]).to_dict())
            jsonFile["params"].append(newParam)
        try:
            self.dump_params(jsonFile)
        except :
            self.logger.error('Cannot dump optimized values!')
        return jsonFile


    def dump_params(self, jsonFile):
        if self.botName:
            botFileName = self.botName + ".json"
            try:
                with open(path.join(self.settings.SIGNALS_DIR , botFileName), 'w') as json_data_file:
                    json.dump(jsonFile, json_data_file)
            except:
                self.logger.error(f"Cannot dump into {botFileName}!")
                raise RuntimeError(f"Cannot dump into {botFileName}!")
        else:
            strategyFileName = self.strategyName + ".json"
            try:
                with open(path.join(self.settings.STRATEGIES_DIR , strategyFileName), 'w') as json_data_file:
                    json.dump(jsonFile, json_data_file)
            except:
                self.logger.error(f"Cannot dump into {strategyFileName}!")
                raise RuntimeError(f"Cannot dump into {strategyFileName}!")

    def calc_history_needed(self):
        max = 1
        if self.optimization:
            for j in self.inputs:
                for i in j:
                    if i.historyNeeded:
                        if i.value > max:
                            max = i.value
        else:    
            for i in self.inputs[0]:
                if i.historyNeeded:
                    if i.value > max:
                        max = i.value
        return max * Utility.array[self.timeFrame] * 60
        
        

        

            

