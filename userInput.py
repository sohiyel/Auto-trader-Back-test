import json
from paramInput import ParamInput
import itertools
import numpy as np
from random import shuffle
import time

class UserInput():
    def __init__(self, pair, timeFrame, strategyName, botName, optimization = False, randomInput = False) -> None:
        self.pair = pair
        self.timeFrame = timeFrame
        self.strategyName = strategyName
        self.botName = botName
        self.optimization = optimization
        self.step = 0
        self.inputs = []
        self.randomInput = randomInput
        if botName:
            self.inputs= self.getBotInputs()
        else:
            self.inputs = self.getStrategyInputs(strategyName)
        if randomInput:
            shuffle(self.inputs)


    def getStrategyInputs(self, strategyName):
        json_data_file = open("strategies/{jsonName}.json".format(jsonName = strategyName))
        jsonFile = json.load(json_data_file)
        inputs = []
        if self.optimization:
            for i in jsonFile["optimization"]["inputs"]:
                pi = ParamInput(i["name"], i["value"], i["strategy"], i["minValue"], i["maxValue"], i["step"], i["optimization"])
                if pi.optimization:
                    strategyInputs = []
                    for i in np.arange(pi.minValue, pi.maxValue, pi.step):
                        strategyInputs.append(ParamInput(pi.name, i, pi.strategy , pi.minValue, pi.maxValue, pi.step, pi.optimization))
                    inputs.append(strategyInputs)
                else:
                    inputs.append([pi])
        else:    
            params = jsonFile["params"][0]
            for p in jsonFile["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    params = p
            for i in params["inputs"]:
                pi = ParamInput(i["name"], i["value"],i["strategy"])
                inputs.append([pi])
        
        json_data_file.close()
        return list( itertools.product( *inputs ) )

    def getBotInputs(self):
        json_data_file = open("signals/{jsonName}.json".format(jsonName = self.botName))
        jsonFile = json.load(json_data_file)
        inputs = []
        if self.optimization:
            for i in jsonFile["optimization"]["inputs"]:
                pi = ParamInput(i["name"], i["value"], i["strategy"], i["minValue"], i["maxValue"], i["step"], i["optimization"])
                if pi.optimization:
                    strategyInputs = []
                    for i in np.arange(pi.minValue, pi.maxValue, pi.step):
                        strategyInputs.append(ParamInput(pi.name, i, pi.strategy , pi.minValue, pi.maxValue, pi.step, pi.optimization))
                    inputs.append(strategyInputs)
                else:
                    inputs.append([pi])
        else:    
            params = jsonFile["params"][0]
            for p in jsonFile["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    params = p
            for i in params["inputs"]:
                pi = ParamInput(i["name"], i["value"],i["strategy"])
                inputs.append([pi])
        
        json_data_file.close()
        return list( itertools.product( *inputs ) )

    def getCurrentInput(self):
        return self.inputs[self.step]

    def getStrategyNames(self):
        strategyNames = []
        json_data_file = open("signals/{jsonName}.json".format(jsonName = self.botName))
        jsonFile = json.load(json_data_file)
        for s in jsonFile["strategies"]:
            strategyNames.append(s["strategy"])
        json_data_file.close()
        return strategyNames

    def getInputNames(self):
        names = []
        if self.botName:
            with open("signals/{jsonName}.json".format(jsonName = self.botName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
        else:
            with open("strategies/{jsonName}.json".format(jsonName = self.strategyName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)

        params = jsonFile["params"][0]
        for i in params["inputs"]:
            names.append( (i["name"],i["strategy"]) )
        json_data_file.close()
        return names

    def writeOptimizedValues(self, report):
        inputNames = []
        if self.botName:
            with open("signals/{jsonName}.json".format(jsonName = self.botName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
        else:
            with open("strategies/{jsonName}.json".format(jsonName = self.strategyName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
        inputNames = self.getInputNames()

        paramExist = False
        for idx,param in enumerate(jsonFile["params"]):
            if param["time_frame"] == self.timeFrame and param["pair"] == self.pair:
                paramExist = True
                for n in inputNames:
                    value = float(report[n[1] + "_" + n[0]])
                    inputExist = False
                    for i in range(len(jsonFile["params"][idx]["inputs"])):
                        if jsonFile["params"][idx]["inputs"][i]["name"] == n[0]:
                            jsonFile["params"][idx]["inputs"][i]["value"] = value
                            inputExist = True
                            break
                    if not inputExist:
                        newInput = ParamInput(n[0], value, n[1])
                        jsonFile["params"][idx]["inputs"].append(newInput.to_dict())

        if not paramExist:
            newParam = {}
            newParam["time_frame"] = self.timeFrame
            newParam["pair"] = self.pair
            newParam["inputs"] = []
            for n in inputNames:
                value = float(report[n[1] + "_" + n[0]])
                newParam["inputs"].append(ParamInput(n[0], value, n[1]).to_dict())
            jsonFile["params"].append(newParam)

        jsonFile["optimization"]["optimization_date"] = time.strftime("%Y-%m-%d_%H:%M:%S")

        if self.botName:
            with open("signals/{jsonName}.json".format(jsonName = self.botName), 'w') as json_data_file:
                json.dump(jsonFile, json_data_file)
        else:
            with open("strategies/{jsonName}.json".format(jsonName = self.strategyName), 'w') as json_data_file:
                json.dump(jsonFile, json_data_file)
        
        

        

            

