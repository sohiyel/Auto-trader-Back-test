from src.exchanges.baseExchange import BaseExchange
import ccxt
from src.logManager import get_logger

class Okex(BaseExchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        self.exchange = ccxt.okex()
        self.exchange.set_sandbox_mode(sandBox)
        self.logger = get_logger(__name__, settings)
        self.authorize()
        
    def fetch_balance(self):
        try:
            response = self.exchange.fetch_balance()
            self.logger.debug("Fetch balance response: ", response)
            if response['info']['code'] == '0':
                return {
                    'Equity' : float(response['info']['data'][0]['details'][0]['availEq']),
                    'Balance' : float(response['info']['data'][0]['details'][0]['cashBal'])
                }
            else:
                self.logger.error("Problem in getting account equity!")
                self.logger.error (response)
                return False
        except Exception as e:
            self.logger.error("Cannot fetch balance from ccxt!"+ str(e))
            return False

    def create_market_order(self, symbol, side, amount, price=None, params={}):
        nparams = {
            'tdMode': 'isolated'
        }
        return self.exchange.create_market_order(symbol, side, amount, nparams)


