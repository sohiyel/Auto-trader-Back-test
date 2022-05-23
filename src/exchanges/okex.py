from exchanges.base_exchange import base_exchange
from src.exchanges.kucoin import Kucoin
import requests
import asyncio
import ccxt

from src.utility import Utility
from datetime import datetime
import time
from src.logManager import get_logger

class okex(base_exchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        super().__init__(sandBox)
        self.exchange = ccxt.okex()
        self.exchange.set_sandbox_mode(sandBox)
        self.logger = get_logger(__name__, settings)
        
    def fetch_balance(self):
        try:
            response = self.exchange.fetch_balance()
            if response['info']['code'] == '0':
                return {
                    'Equity' : response['info']['data']['accountEquity'],
                    'Balance' : response['info']['data']['availableBalance']
                }
            else:
                self.logger.error("Problem in getting account equity!")
                self.logger.error (response)
                return False
        except:
            self.logger.error("Cannot fetch balance from ccxt!")
            return False


