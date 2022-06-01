from src.exchanges.exchange import Exchange
from src.exchanges.kucoinFutures import KucoinFutures
import json
from src.utility import Utility
import os
from src.logManager import LogService
from src.settings import Settings

class Markets():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.exchange = settings.exchange_service #Exchange(settings).exchange
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        self.markets = ""
        if os.path.exists(self.settings.MARKET_JSON_PATH):
            self.read_file()
        else:
            self.load_market()
            self.write_to_file()

    def load_market(self):
        self.markets = self.exchange.load_markets()

    def write_to_file(self):
        try:
            json_data_file = open(self.settings.MARKET_JSON_PATH, "w")
            json.dump(self.markets, json_data_file)
            json_data_file.close()
        except:
            self.logger.error("Cannot write market data to file!")

    def read_file(self):
        try:
            json_data_file = open(self.settings.MARKET_JSON_PATH, "r")
            json_file = json.load(json_data_file)
            json_data_file.close()
            self.markets = json_file
        except:
            self.logger.error("Cannot read market data from file!")

    def get_contract_size(self, pair):
        try:
            ePair = self.exchange.change_symbol_for_markets(pair) #Utility.get_exchange_format(pair+":USDT")
            for i in self.markets:
                if ePair in i:
                    self.logger.debug(i)
                    ePair = i
                    break
            marketData = self.markets[ePair]
            return marketData['contractSize']
        except Exception as e:
            self.logger.error(f"Cannot get contract size of {ePair}" + str(e))


if __name__ == '__main__':
    settings = Settings('sohiyel')
    settings.exchange_service = Exchange(settings).exchange
    market = Markets(settings)
    # market.load_market()
    # market.write_to_file()
    market.logger.debug(market.get_contract_size("trx_USDT"))