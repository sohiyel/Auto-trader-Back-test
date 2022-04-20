from pprint import isreadable
from src.data import DataService
from src.tfMap import tfMap
from src.trader import Trader
from src.userInput import UserInput
import pandas as pd
from pprint import pprint
import time
from datetime import datetime
from src.tradeIndex import TradeIndex
from src.exchanges.kucoinFutures import KucoinFutures
from src.exchanges.kucoinSpot import  KucoinSpot
import asyncio
import concurrent.futures
import sys
class TradeRunner():
    def __init__(self) -> None:
        self.tradeIndexList = TradeIndex().indexes
        self.exchange = KucoinFutures(sandBox = False)
        self.exchange.authorize()
        self.trades = []

    def initialize_indexes(self, index):
        trader = Trader(index,self.exchange.exchange)
        self.trades.append(trader)
        print  (f"--------- Initialized :{index.pair} ---------")
        startTime = time.time()
        counter = 0
        while True:
            deltaTime = (time.time() - startTime)
            if int(deltaTime % (tfMap.array[index.timeFrame] * 60)) == 0:
                trader.mainloop()
            if int(deltaTime % (tfMap.array[index.timeFrame] * 20)) == 0:
                trader.check_continue()
            time.sleep(1)

if __name__ == '__main__':
    tradeRunner = TradeRunner()
    tradeRunner.initialize_indexes(tradeRunner.tradeIndexList[0])
    # with concurrent.futures.ThreadPoolExecutor() as executor:        
    #     executor.map(tradeRunner.initialize_indexes,tradeRunner.tradeIndexList)

