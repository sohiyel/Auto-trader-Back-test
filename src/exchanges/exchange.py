
import ccxt
from src.exchanges.okex import okex
from src.exchanges.kucoinFutures import KucoinFutures
from src.utility import Utility
from src.logManager import get_logger

class exchange():
    def __init__(self, settings):
        self.settings = settings
        self.sandBox = settings.sandBox
        self.exchange = self.init_exchange()
        self.exchange.set_sandbox_mode(self.sandBox)
        self.logger = get_logger(__name__, settings)

    def fetch_ohlcv(self, pair, timeframe):
        return self.exchange.fetch_ohlcv(pair, timeframe)
    
    def fetch_ohlcv(self, pair, timeframe, since):
        return self.exchange.fetch_ohlcv(pair, timeframe, since)
    
    def init_exchange(self):
        print("exchange : " + self.settings.exchange)
        if self.settings.exchange == 'kucoinfutures':
            return KucoinFutures()
        elif self.settings.exchange == 'okex':
            return okex()
        else:
            return KucoinFutures()
