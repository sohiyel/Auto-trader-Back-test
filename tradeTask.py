import json

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

    def read_toDo(self):
        with open("task.json", "w") as json_data_file:
            jsonFile = json.load(json_data_file)
            if len(jsonFile["To_Do"]) > 0:
                self.pair = jsonFile["To_Do"][0]["pair"]
                self.timeFrame = jsonFile["To_Do"][0]["timeFrame"]
                self.strategyName = jsonFile["To_Do"][0]["strategyName"]
                self.botName = jsonFile["To_Do"][0]["botName"]
                self.startAt = jsonFile["To_Do"][0]["startAt"]
                self.endAt = jsonFile["To_Do"][0]["endAt"]
                self.volume = jsonFile["To_Do"][0]["volume"]
                self.initialCapital = jsonFile["To_Do"][0]["initialCapital"]
                self.market = jsonFile["To_Do"][0]["market"]
                self.optimization = jsonFile["To_Do"][0]["optimization"]
                self.randomInputs = jsonFile["To_Do"][0]["randomInput"]
                self.numberOfInputs = jsonFile["To_Do"][0]["numberOfInput"]

                del jsonFile["To_Do"][0]
                json.dump(jsonFile, json_data_file)
            else:
                print("There is no tasks in the queue!")
