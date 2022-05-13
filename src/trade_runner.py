from pprint import isreadable
from src.utility import Utility
from src.trader import Trader
from pprint import pprint
import time
from src.tradeIndex import TradeIndex
from src.exchanges.kucoinFutures import KucoinFutures
import concurrent.futures

class TradeRunner():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.tradeIndexList = TradeIndex(settings).indexes
        self.exchange = KucoinFutures(settings, sandBox = False)
        self.exchange.authorize()
        self.trades = []

    def initialize_indexes(self, index):
        trader = Trader(index,self.exchange.exchange, self.settings)
        self.trades.append(trader)
        print  (f"--------- Initialized :{index.pair} ---------")
        startTime = time.time()
        counter = 0
        while True:
            deltaTime = (time.time() - startTime)
            if int(deltaTime % (Utility.array[index.timeFrame] * 60)) == 0:
                trader.mainloop()
            if int(deltaTime % (Utility.array[index.timeFrame] * 20)) == 0:
                trader.check_continue()
            time.sleep(1)

if __name__ == '__main__':
    tradeRunner = TradeRunner()
    tradeRunner.initialize_indexes(tradeRunner.tradeIndexList[0])
    # with concurrent.futures.ThreadPoolExecutor() as executor:        
    #     executor.map(tradeRunner.initialize_indexes,tradeRunner.tradeIndexList)

