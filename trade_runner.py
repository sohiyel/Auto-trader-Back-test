from pprint import isreadable
from data import DataService
from tfMap import tfMap
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
        self.exchange = KucoinFutures(sandBox = False)
        self.exchange.authorize()

    def initialize_indexes(self, index):
        trader = Trader(index,self.exchange.exchange)
        print  (f"--------- Initialized :{index.pair} ---------")
        while True:
            trader.mainloop()
            time.sleep(tfMap.array[index.timeFrame] * 60)

if __name__ == '__main__':
    tradeRunner = TradeRunner()
    tradeRunner.initialize_indexes(tradeRunner.tradeIndexList[0])
    # with concurrent.futures.ThreadPoolExecutor() as executor:        
    #     executor.map(tradeRunner.initialize_indexes,tradeRunner.tradeIndexList)

