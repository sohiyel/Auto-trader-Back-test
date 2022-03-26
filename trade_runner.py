from pprint import isreadable
from data import DataService
from trader import Trader
from userInput import UserInput
import pandas as pd
from pprint import pprint
import time
from datetime import datetime
from tradeIndex import TradeIndex
from kucoinFutures import KucoinFutures
from kucoinSpot import  KucoinSpot
import asyncio
import concurrent.futures
import sys
class TradeRunner():
    def __init__(self) -> None:
        self.tradeIndexList = TradeIndex().indexes
        self.indexes = []
        self.exchange = KucoinFutures(sandBox = True)
        self.exchange.authorize()

    def initialize_indexes(self, index):
        trader = Trader(index,self.exchange.ccxt)
        trader.mainloop()
        self.indexes.append(trader)
        print  (f"--------- Initialized :{index.pair} ---------")
        time.sleep(1)

    def run_trade(self):
        pass

if __name__ == '__main__':
    tradeRunner = TradeRunner()
    with concurrent.futures.ThreadPoolExecutor() as executor:        
        executor.map(tradeRunner.initialize_indexes,tradeRunner.tradeIndexList)

