from pprint import isreadable
from data import DataService
from trader import Trader
from userInput import UserInput
import pandas as pd
from pprint import pprint
import time
from datetime import datetime
from tradeIndex import TradeIndex

class TradeRunner():
    def __init__(self) -> None:
        self.tradeIndexList = TradeIndex().indexes

    def run_trade(self):
        for index in self.tradeIndexList:
            print  (f"--------- start check on :{index.pair} ---------")
            trader = Trader(index)
            print  (f"--------- end check on :{index.pair} ---------")

if __name__ == '__main__':
    tradeRunner = TradeRunner()
    while True:
        tradeRunner.run_trade()
        time.sleep(5)

