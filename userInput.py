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
            self.inputs= self.getBotInputs(botName)
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
                pi = ParamInput(i["name"], i["title"], i["type"], i["value"], i["from"], i["to"], i["step"], i["optimized"], i["strategy"])
                if pi.optimization:
                    strategyInputs = []
                    for i in np.arange(pi.minValue, pi.maxValue, pi.step):
                        strategyInputs.append(ParamInput(pi.name, pi.title, pi.type, i, pi.minValue, pi.maxValue, pi.step, pi.optimization, pi.strategy))
                    inputs.append(strategyInputs)
                else:
                    inputs.append([pi])
        else:    
            params = jsonFile["params"][0]
            for p in jsonFile["params"]:
                if p["time_frame"] == self.timeFrame and p["pair"] == self.pair:
                    params = p
            for i in params["inputs"]:
                pi = ParamInput(i["name"], i["title"], i["type"], i["value"],i["strategy"])
                inputs.append([pi])
        
        json_data_file.close()
        return list( itertools.product( *inputs ) )

    def getBotInputs(self, botName):
        strategyNames = []
        inputs = []
        json_data_file = open("signals/{jsonName}.json".format(jsonName = botName))
        jsonFile = json.load(json_data_file)
        for s in jsonFile["strategies"]:
            strategyNames.append(s["strategy"])
        json_data_file.close()
        for strategy in strategyNames:
            inputs.append( self.getStrategyInputs(strategy) )
        
        return list( itertools.product( *inputs ) )

    def getCurrentInput(self):
        return self.inputs[self.step]