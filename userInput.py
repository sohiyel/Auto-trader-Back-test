import json
from paramInput import ParamInput
import itertools
import numpy as np
from random import shuffle

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
            params = jsonFile["optimization"][0]
            for p in jsonFile["optimization"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    params = p
            
            for i in params["inputs"]:
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
            params = jsonFile["optimization"][0]
            for p in jsonFile["optimization"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    params = p
            
            for i in params["inputs"]:
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

    def getInputNames(self, strategyName):
        names = []
        json_data_file = open("strategies/{jsonName}.json".format(jsonName = strategyName))
        jsonFile = json.load(json_data_file)
        params = jsonFile["params"][0]
        for i in params["inputs"]:
            names.append( i["name"] )
        json_data_file.close()
        return names

    def writeOptimizedValues(self, report):
        inputNames = []
        if self.botName:
            strategyNames = self.getStrategyNames()
            with open("signals/{jsonName}.json".format(jsonName = self.botName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
            pairExist = False
            for idx,p in enumerate(jsonFile["optimization"]):
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    pairExist = True
                    for strategyName in strategyNames:
                        inputNames = self.getInputNames(strategyName)
                        for n in inputNames:
                            if (n == "sl_percent" or n == "tp_percent") and strategyName != self.botName:
                                continue
                            value = float(report[strategyName + "_" + n])
                            inputExist = False
                            for i in range(len(jsonFile["optimization"][idx]["inputs"])):
                                if jsonFile["optimization"][idx]["inputs"][i]["name"] == n:
                                    jsonFile["optimization"][idx]["inputs"][i]["value"] = value
                                    inputExist = True
                                    break
                            if not inputExist:
                                newInput = ParamInput(n, value, strategyName)
                                jsonFile["optimization"][idx]["inputs"].append(newInput.to_dict())
            if not pairExist:
                newPair = {}
                newPair["time_frame"] = self.timeFrame
                newPair["pair"] = self.pair
                newPair["inputs"] = []
                for strategyName in strategyNames:
                    inputNames = self.getInputNames(strategyName)
                    for n in inputNames:
                        inputName = strategyName + "_" + n
                        value = float(report[inputName])
                        newInput = ParamInput(n, value, strategyName)
                        newPair["inputs"].append(newInput.to_dict())
                jsonFile["optimization"].append(newPair)

            with open("signals/{jsonName}.json".format(jsonName = self.botName), 'w') as json_data_file:
                json.dump(jsonFile, json_data_file)

        else:
            with open("strategies/{jsonName}.json".format(jsonName = self.strategyName), 'r+') as json_data_file:
                jsonFile = json.load(json_data_file)
            pairExist = False
            for idx,p in enumerate(jsonFile["optimization"]):
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    pairExist = True
                    inputNames = self.getInputNames(self.strategyName)
                    for n in inputNames:
                        value = float(report[self.strategyName + "_" + n])
                        inputExist = False
                        for i in range(len(p["inputs"])):
                            if jsonFile["optimization"][idx]["inputs"][i]["name"] == n:
                                jsonFile["optimization"][idx]["inputs"][i]["value"] = value
                                inputExist = True
                                break
                        if not inputExist:
                            newInput = ParamInput(n, value, strategyName)
                            jsonFile["optimization"][idx]["inputs"].append(newInput.to_dict())
                    break
            if not pairExist:
                newPair = {}
                newPair["time_frame"] = self.timeFrame
                newPair["pair"] = self.pair
                newPair["inputs"] = []
                inputNames = self.getInputNames(self.strategyName)
                for n in inputNames:
                    inputName = self.strategyName + "_" + n
                    value = float(report[inputName])
                    newInput = ParamInput(n, value, self.strategyName)
                    newPair["inputs"].append(newInput.to_dict())
                jsonFile["optimization"].append(newPair)    

            with open("strategies/{jsonName}.json".format(jsonName = self.strategyName), 'w') as json_data_file:
                json.dump(jsonFile, json_data_file)

