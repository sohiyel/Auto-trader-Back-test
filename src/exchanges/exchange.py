
import ccxt
from src.exchanges.okex import Okex
from src.exchanges.kucoinFutures import KucoinFutures
from src.utility import Utility
from src.logManager import get_logger

class Exchange():
    def __init__(self, settings):
        self.settings = settings
        self.sandBox = settings.sandbox
        self.logger = get_logger(__name__, settings)
        self.logger.info("exchange : " + self.settings.exchange)
        if self.settings.exchange == 'kucoinfutures':
            self.exchange = KucoinFutures(self.settings)
        elif self.settings.exchange == 'okex':
            self.exchange = Okex(self.settings)
        else:
            self.exchange = KucoinFutures(self.settings)
