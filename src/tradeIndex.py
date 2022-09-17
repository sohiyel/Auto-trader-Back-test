import json
from src.userInput import UserInput
from src.utility import Utility
from src.logManager import LogService

class TradeIndex():
    def __init__(self, settings) -> None:
        self.indexes = []
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        try:
            with open(settings.TRADES_PATH,"r") as json_data_file:
                self.jsonFile = json.load(json_data_file)
                ptss = self.jsonFile["trades"]["pts"]
                for pts in ptss:
                    userInput = UserInput( pair = pts["pair"], 
                                                    timeFrame = Utility.unify_timeframe(pts["tf"], settings.exchange),
                                                    strategyName = pts["strategy"],
                                                    botName = pts["bot"],
                                                    side = pts["long_short"],
                                                    leverage = pts["leverage"],
                                                    mOfContractSize = pts["amount_multiple_of_contract_size"],
                                                    amount = pts["amount_stake"],
                                                    ratioAmount = pts["amout_balance_ratio"],
                                                    settings= settings)
                    userInput.find_inputs()
                    self.indexes.append( userInput )
        except:
            self.logger.error("Error in reading trades.json!")                                                
            
            