
from src.logManager import get_logger
import configparser

class BaseExchange():
    def __init__(self,settings, sandBox = False):
        self.settings = settings
        self.logger = get_logger(__name__, settings)
        self.authorize()

    def fetch_ohlcv(self, pair, timeframe, since=""):
        if since:
            return self.exchange.fetch_ohlcv(pair, timeframe, since)
        return self.exchange.fetch_ohlcv(pair, timeframe)
    
    def fetch_order_book(self, pair):
        return self.exchange.fetch_order_book(pair)

    def create_market_order(self, symbol, side, amount, price=None, params={}):
        return self.exchange.create_market_order(symbol, side, amount, params)

    def fetch_positions(self, symbols=None, params={}):
        return self.exchange.fetch_positions()

    def load_markets(self):
        return self.exchange.load_markets()


    def authorize(self):
        cfg = configparser.ConfigParser()
        try:
            cfg.read(self.settings.API_PATH)
            self.exchange.apiKey = cfg.get('KEYS','api_key')
            self.exchange.secret = cfg.get('KEYS', 'api_secret')
            self.exchange.password = cfg.get('KEYS', 'api_passphrase')
        except Exception as e:
            self.logger.error("Cannot read exchange config file!" + str(e))

    