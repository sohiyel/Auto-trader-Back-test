from kucoinFutures import KucoinFutures
import json
from tfMap import tfMap
import os

class Markets():
    def __init__(self) -> None:
        self.exchange = KucoinFutures(sandBox = False)
        self.exchange.authorize()
        if os.path.exists("settings/markets.json"):
            self.markets = self.read_file()
        else:
            self.markets = self.load_market()
            self.write_to_file()

    def load_market(self):
        return self.exchange.exchange.load_markets()

    def write_to_file(self):
        json_data_file = open("settings/markets.json", "w")
        json.dump(self.markets, json_data_file)
        json_data_file.close()

    def read_file(self):
        json_data_file = open("settings/markets.json", "r")
        json_file = json.load(json_data_file)
        json_data_file.close()
        return json_file

    def get_contract_size(self, pair):
        ePair = tfMap.get_exchange_format(pair)
        return self.markets[ePair]['contractSize']


if __name__ == '__main__':
    print(Markets().get_contract_size("BTC/USDT"))