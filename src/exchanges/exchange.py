import requests
import ccxt
from src.utility import Utility
from src.logManager import get_logger

class exchange():
    def __init__(self,settings, sandBox = False):
        self.settings = settings
        self.exchange = self.init_exchange()
        self.exchange.set_sandbox_mode(sandBox)
        self.logger = get_logger(__name__, settings)

    def fetch_ohlcv(self, pair, timeframe):
        return self.exchange.fetch_ohlcv(pair, timeframe)
    
    def fetch_ohlcv(self, pair, timeframe, since):
        return self.exchange.fetch_ohlcv(pair, timeframe, since)


    def init_exchange(self):
        print("exchange : " + self.settings.exchange)
        if self.settings.exchange == 'kucoinfutures':
            return ccxt.kucoinfutures()
        elif self.settings.exchange == 'kucoin':
            return ccxt.kucoin
        elif self.settings.exchange == 'okex':
            return ccxt.okex()
        else:
            return ccxt.kucoinfutures()
