import json
import time
class TradeTask():
    def __init__(self) -> None:
        self.pair = "BTC-USDT"
        self.timeFrame = "4hour"
        self.strategyName = "RSIStrategy"
        self.botName = "Bot02"
        self.startAt = "2021-01-01 00:00:00"
        self.endAt = "2021-09-01 00:00:00"
        self.volume = 1
        self.initialCapital = 100000
        self.market = "spot"
        self.optimization = False
        self.randomInputs = False
        self.numberOfInputs = 1
        self.jsonFile = ""

    def read_toDo(self):
        with open("tasks.json", "r") as json_data_file:
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

            else:
                print("There is no tasks in the queue!")

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

        with open("tasks.json", "w") as json_data_file:
            del self.jsonFile["To_Do"][0]
            self.jsonFile["Done"].append(task)
            json.dump(self.jsonFile, json_data_file)
