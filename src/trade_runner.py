from src.exchanges.exchange import Exchange
from src.utility import Utility
from src.trader import Trader
import time
from src.tradeIndex import TradeIndex
from src.exchanges.kucoinFutures import KucoinFutures
import concurrent.futures
from src.logManager import LogService

class TradeRunner():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.tradeIndexList = TradeIndex(settings).indexes
        self.exchange = settings.exchange_service #Exchange(settings).exchange
        self.exchange.authorize()
        self.trades = []
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)


    def initialize_indexes(self, index):
        pts = {'pair': index.pair, 'timeFrame': index.timeFrame, 'strategyName': 'NaN'}
        self.logService.set_pts_formatter(pts)
        trader = Trader(index, self.settings)
        self.trades.append(trader)
        self.logger.info  (f"--------- Initialized :{index.pair} ---------")
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

