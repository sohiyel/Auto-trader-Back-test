import json
import time
from account.settings.settings import Settings

class BackTestTask():
    def __init__(self) -> None:
        with open(Settings.TASKS_PATH, "r") as json_data_file:
            self.jsonFile = json.load(json_data_file)
            self.pair = self.jsonFile["default"]["pair"]
            self.timeFrame = self.jsonFile["default"]["timeFrame"]
            self.strategyName = self.jsonFile["default"]["strategyName"]
            self.botName = self.jsonFile["default"]["botName"]
            self.startAt = self.jsonFile["default"]["startAt"]
            self.endAt = self.jsonFile["default"]["endAt"]
            self.volume = self.jsonFile["default"]["volume"]
            self.initialCapital = self.jsonFile["default"]["initialCapital"]
            self.market = self.jsonFile["default"]["market"]
            self.optimization = self.jsonFile["default"]["optimization"]
            self.randomInputs = self.jsonFile["default"]["randomInputs"]
            self.numberOfInputs = self.jsonFile["default"]["numberOfInputs"]

    def read_toDo(self):
        with open(Settings.TASKS_PATH, "r") as json_data_file:
            self.jsonFile = json.load(json_data_file)
            if len(self.jsonFile["To_Do"]) > 0:
                self.pair = self.jsonFile["To_Do"][0]["pair"]
                self.timeFrame = self.jsonFile["To_Do"][0]["timeFrame"]
                self.strategyName = self.jsonFile["To_Do"][0]["strategyName"]
                self.botName = self.jsonFile["To_Do"][0]["botName"]
                self.startAt = self.jsonFile["To_Do"][0]["startAt"]
                self.endAt = self.jsonFile["To_Do"][0]["endAt"]
                self.volume = self.jsonFile["To_Do"][0]["volume"]
                self.initialCapital = self.jsonFile["To_Do"][0]["initialCapital"]
                self.market = self.jsonFile["To_Do"][0]["market"]
                self.optimization = self.jsonFile["To_Do"][0]["optimization"]
                self.randomInputs = self.jsonFile["To_Do"][0]["randomInputs"]
                self.numberOfInputs = self.jsonFile["To_Do"][0]["numberOfInputs"]
                return True

            else:
                print("There is no tasks in the queue!")
                return False

    def done_task(self):
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
        task["doneAt"] = time.strftime("%Y-%m-%d_%H-%M-%S")

        with open(Settings.TASKS_PATH, "w") as json_data_file:
            del self.jsonFile["To_Do"][0]
            self.jsonFile["Done"].append(task)
            json.dump(self.jsonFile, json_data_file)
