from src.exchanges.okexFuture import OkexFuture
from src.exchanges.okexSpot import OkexSpot
from src.exchanges.kucoinFutures import KucoinFutures
from src.exchanges.kucoinSpot import KucoinSpot
from src.logManager import LogService

class Exchange():
    def __init__(self, settings):
        self.settings = settings
        self.sandBox = settings.sandbox
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger
        self.logger.info("exchange : " + self.settings.exchange)
        if self.settings.exchange == 'kucoin_futures':
            self.exchange = KucoinFutures(self.settings)
        elif self.settings.exchange == 'kucoin_spot':
            self.exchange = KucoinSpot(self.settings)
        elif self.settings.exchange == 'okex_future':
            self.exchange = OkexFuture(self.settings)
        elif self.settings.exchange == 'okex_spot':
            self.exchange = OkexSpot(self.settings)
        else:
            self.logger.error("Invalid exchange name!")
            raise ValueError("Invalid exchange name!")
