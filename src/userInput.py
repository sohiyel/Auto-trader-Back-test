import json
from src.paramInput import ParamInput
import itertools
import numpy as np
from random import shuffle
import time
from src.utility import Utility
from os import path

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
        if botName:
            self.inputs= self.get_bot_inputs()
        else:
            self.inputs = self.get_strategy_inputs(strategyName)
        if randomInput:
            shuffle(self.inputs)


    def get_strategy_inputs(self, strategyName):
        strategyFileName = strategyName + ".json"
        json_data_file = open(path.join(self.settings.STRATEGIES_DIR , strategyFileName))
        jsonFile = json.load(json_data_file)
        inputs = []
        if self.optimization:
            for i in jsonFile["optimization"]["inputs"]:
                pi = ParamInput(i["name"], i["value"], i["strategy"], i["historyNeeded"], i["minValue"], i["maxValue"], i["step"], i["optimization"])
                if pi.optimization:
                    strategyInputs = []
                    for i in np.arange(pi.minValue, pi.maxValue, pi.step):
                        strategyInputs.append(ParamInput(pi.name, i, pi.strategy, pi.historyNeeded , pi.minValue, pi.maxValue, pi.step, pi.optimization))
                    inputs.append(strategyInputs)
                else:
                    inputs.append([pi])
        else:    
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
        
        json_data_file.close()
        return list( itertools.product( *inputs ) )

    def get_bot_inputs(self):
        botFileName = self.botName + ".json"
        json_data_file = open(path.join(self.settings.SIGNALS_DIR , botFileName))
        jsonFile = json.load(json_data_file)
        inputs = []
        if self.optimization:
            for i in jsonFile["optimization"]["inputs"]:
                pi = ParamInput(i["name"], i["value"], i["strategy"], i["historyNeeded"], i["minValue"], i["maxValue"], i["step"], i["optimization"])
                if pi.optimization:
                    strategyInputs = []
                    for i in np.arange(pi.minValue, pi.maxValue, pi.step):
                        strategyInputs.append(ParamInput(pi.name, i, pi.strategy, pi.historyNeeded, pi.minValue, pi.maxValue, pi.step, pi.optimization))
                    inputs.append(strategyInputs)
                else:
                    inputs.append([pi])
        else:    
            params = jsonFile["params"][0]
            for p in jsonFile["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    params = p
            for i in params["inputs"]:
                pi = ParamInput(i["name"], i["value"],i["strategy"], i["historyNeeded"])
                inputs.append([pi])
        
        json_data_file.close()
        return list( itertools.product( *inputs ) )

    def get_current_input(self):
        return self.inputs[self.step]

    def get_strategy_names(self):
        strategyNames = []
        botFileName = self.botName + ".json"
        json_data_file = open(path.join(self.settings.SIGNALS_DIR , botFileName))
        jsonFile = json.load(json_data_file)
        for s in jsonFile["strategies"]:
            strategyNames.append(s["strategy"])
        json_data_file.close()
        return strategyNames

    def get_input_names(self):
        names = []
        if self.botName:
            botFileName = self.botName + ".json"
            with open(path.join(self.settings.SIGNALS_DIR , botFileName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
        else:
            strategyFileName = self.strategyName + ".json"
            with open(path.join(self.settings.STRATEGIES_DIR , strategyFileName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)

        params = jsonFile["params"][0]
        for i in params["inputs"]:
            names.append( (i["name"],i["strategy"],i["historyNeeded"]) )
        json_data_file.close()
        return names

    def write_optimized_values(self, report):
        inputNames = []
        if self.botName:
            botFileName = self.botName + ".json"
            with open(path.join(self.settings.SIGNALS_DIR , botFileName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
        else:
            strategyFileName = self.strategyName + ".json"
            with open(path.join(self.settings.STRATEGIES_DIR , strategyFileName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
        inputNames = self.get_input_names()

        paramExist = False
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

        if self.botName:
            botFileName = self.botName + ".json"
            with open(path.join(self.settings.SIGNALS_DIR , botFileName), 'w') as json_data_file:
                json.dump(jsonFile, json_data_file)
        else:
            strategyFileName = self.strategyName + ".json"
            with open(path.join(self.settings.STRATEGIES_DIR , strategyFileName), 'w') as json_data_file:
                json.dump(jsonFile, json_data_file)

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
        
        

        

            

