import json
from userInput import UserInput

class TradeIndex():
    def __init__(self) -> None:
        self.indexes = []
        with open("settings/trades.js","r") as json_data_file:
            self.jsonFile = json.load(json_data_file)
            ptss = self.jsonFile["trades"]["pts"]
            for pts in ptss:
                self.indexes.append( UserInput( pair = pts["pair"], 
                                                timeFrame = pts["tf"], 
                                                strategyName = pts["strategy"],
                                                botName = pts["bot"],
                                                side = pts["long_short"],
                                                amount = pts["stake_amount"],
                                                ratioAmount = pts["tradeable_balance_ratio"]))
            
            