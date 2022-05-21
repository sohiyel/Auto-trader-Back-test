import json
import time
import os
from src.utility import Utility
from src.logManager import get_logger
class BackTestTask():
    def __init__(self,settings) -> None:
        self.settings = settings
        self.pair = ""
        self.timeFrame = ""
        self.strategyName = ""
        self.botName = ""
        self.startAt = ""
        self.endAt = ""
        self.volume = ""
        self.initialCapital = ""
        self.market = ""
        self.optimization = ""
        self.randomInputs = ""
        self.numberOfInputs = ""
        self.logger = get_logger(__name__, settings)

    def read_toDo(self):
        if os.path.exists(self.settings.TASKS_PATH):
            try:
                with open(self.settings.TASKS_PATH, "r") as json_data_file:
                    self.jsonFile = json.load(json_data_file)
                    if len(self.jsonFile["To_Do"]) > 0:
                        if "pair" in self.jsonFile["To_Do"][0]:
                            self.pair = self.jsonFile["To_Do"][0]["pair"]
                        else:
                            self.pair = ""
                        if "timeFrame" in self.jsonFile["To_Do"][0]:
                            self.timeFrame = Utility.unify_timeframe(self.jsonFile["To_Do"][0]["timeFrame"], self.settings.exchange)
                        else:
                            self.timeFrame = ""
                        if "strategyName" in self.jsonFile["To_Do"][0]:
                            self.strategyName = self.jsonFile["To_Do"][0]["strategyName"]
                        else:
                            self.strategyName = ""
                        if "botName" in self.jsonFile["To_Do"][0]:
                            self.botName = self.jsonFile["To_Do"][0]["botName"]
                        else:
                            self.botName = ""
                        if "startAt" in self.jsonFile["To_Do"][0]:
                            self.startAt = self.jsonFile["To_Do"][0]["startAt"]
                        else:
                            self.startAt = ""
                        if "endAt" in self.jsonFile["To_Do"][0]:
                            self.endAt = self.jsonFile["To_Do"][0]["endAt"]
                        else:
                            self.endAt = ""
                        if "volume" in self.jsonFile["To_Do"][0]:
                            self.volume = self.jsonFile["To_Do"][0]["volume"]
                        else:
                            self.volume = ""
                        if "initialCapital" in self.jsonFile["To_Do"][0]:
                            self.initialCapital = self.jsonFile["To_Do"][0]["initialCapital"]
                        else:
                            self.initialCapital = ""
                        if "market" in self.jsonFile["To_Do"][0]:
                            self.market = self.jsonFile["To_Do"][0]["market"]
                        else:
                            self.market = ""
                        if "optimization" in self.jsonFile["To_Do"][0]:
                            self.optimization = self.jsonFile["To_Do"][0]["optimization"]
                        else:
                            self.optimization = ""
                        if "randomInputs" in self.jsonFile["To_Do"][0]:
                            self.randomInputs = self.jsonFile["To_Do"][0]["randomInputs"]
                        else:
                            self.randomInputs = ""
                        if "numberOfInputs" in self.jsonFile["To_Do"][0]:
                            self.numberOfInputs = self.jsonFile["To_Do"][0]["numberOfInputs"]
                        else:
                            self.numberOfInputs = ""
                        checked, error = self.check_task()
                        if checked:
                            return True
                        else:
                            self.done_task(error)
                            return False

                    else:
                        self.logger.warning("There is no tasks in the queue!")
                        return False
            except:
                self.logger.error("-------------Cannot open tasks.json!-------------")    
        else:
            self.logger.critical("-------------There is no tasks.json in your account!-------------")

    def check_task(self):
        if not (self.pair and self.timeFrame and self.startAt and\
            self.endAt and self.volume and self.initialCapital and self.market):
            self.logger.error("-------------Insufficient task parameters!-------------")    
            return (False,"Insufficient task parameters")
        if self.randomInputs:
            if not self.numberOfInputs:
                self.logger.error("-------------Number of inputs is required for random input!-------------")    
                return (False,"Number of inputs is required for random input")
        if not self.timeFrame in Utility.array.keys():
            self.logger.error("-------------Timeframe of this task is not valid!-------------")
            return (False,"Timeframe of this task is not valid")
        if self.botName:
            if not os.path.exists(os.path.join(self.settings.SIGNALS_DIR, self.botName+".json")):
                self.logger.error("-------------Bot file does not exists!-------------")
                return (False,"Bot file does not exists")
        else:
            if not os.path.exists(os.path.join(self.settings.STRATEGIES_DIR, self.strategyName+".json")):
                self.logger.error("-------------Strategy file does not exists!-------------")
                return (False,"Strategy file does not exists")
        if self.startAt > self.endAt:
            self.logger.error("-------------StartAt and EndAt are not valid!-------------")    
            return (False,"StartAt and EndAt are not valid")
        if not self.market in ['spot', 'futures']:
            self.logger.error("-------------This market type in not valid!-------------")    
            return (False,"This market type in not valid")
        return (True,"ok")
        
    def done_task(self, error=""):
        task = {}
        task["pair"] = self.pair
        task["timeFrame"] = self.timeFrame
        task["strategyName"] = self.strategyName
        task["botName"] = self.botName
        task["startAt"] = self.startAt
        task["endAt"] = self.endAt
        task["volume"] = self.volume
        task["initialCapital"] = self.initialCapital
        task["market"] = self.market
        task["optimization"] = self.optimization
        task["randomInputs"] = self.randomInputs
        task["numberOfInputs"] = self.numberOfInputs
        if error:
            task["error"] = error
        else:
            task["doneAt"] = time.strftime("%Y-%m-%d_%H-%M-%S")

        with open(self.settings.TASKS_PATH, "w") as json_data_file:
            del self.jsonFile["To_Do"][0]
            self.jsonFile["Done"].append(task)
            json.dump(self.jsonFile, json_data_file)
