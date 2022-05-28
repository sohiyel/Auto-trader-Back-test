from django.conf import settings
from src.exchanges.exchange import Exchange
from src.exchanges.kucoinFutures import KucoinFutures
import json
from src.utility import Utility
import os
from src.logManager import get_logger
from src.settings import Settings

class Markets():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.exchange = settings.exchange_service #Exchange(settings).exchange
        self.exchange.authorize()
        self.logger = get_logger(__name__, settings)
        if os.path.exists(self.settings.MARKET_JSON_PATH):
            self.markets = self.read_file()
        else:
            self.markets = self.load_market()
            self.write_to_file()

    def load_market(self):
        return self.exchange.load_markets()

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
            return json_file
        except:
            self.logger.error("Cannot read market data from file!")

    def get_contract_size(self, pair):
        try:
            ePair = Utility.get_exchange_format(pair+":USDT")
            return self.markets[ePair]['contractSize']
        except Exception as e:
            self.logger.error(f"Cannot get contract size of {ePair}" + str(e))


if __name__ == '__main__':
    settings = Settings('sohiyel')
    market = Markets(settings)
    market.load_market()
    market.write_to_file()