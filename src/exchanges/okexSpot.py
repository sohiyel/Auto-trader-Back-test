from src.exchanges.baseExchange import BaseExchange
import ccxt
from src.logManager import LogService
import configparser
from math import floor
from src.utility import Utility

class OkexSpot(BaseExchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        self.exchange = ccxt.okex5()
        self.exchange.options['createMarketBuyOrderRequiresPrice'] = False
        self.exchange.options['defaultType'] = 'future'
        self.exchange.set_sandbox_mode(sandBox)
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)

    def get_second_currency(self, symbol):
        symbols = symbol.split("-")
        for i in symbols:
            if i != self.settings.baseCurrency:
                return i

    def fetch_balance(self, symbol=""):
        if symbol:
            currency = self.get_second_currency(symbol)
        else:
            currency = self.settings.baseCurrency
        try:
            response = self.exchange.fetch_balance()
            self.logger.debug("Fetch balance response: ", response)
            if response['info']['code'] == '0':
                try:
                    return {
                        'Equity' : Utility.truncate(float(response[currency]['free']),1),
                        'Balance' : Utility.truncate(float(response[currency]['total']),1)
                    }
                except:
                    return {
                        'Equity' : 0,
                        'Balance' : 0
                    }
            else:
                self.logger.error("Problem in getting account equity!")
                self.logger.error (response)
                return False
        except Exception as e:
            self.logger.error("Cannot fetch balance from ccxt!"+ str(e))
            return False

    def authorize(self):
        cfg = configparser.ConfigParser()
        try:
            cfg.read(self.settings.API_PATH)
            self.exchange.apiKey = cfg.get('KEYS','api_key')
            self.exchange.secret = cfg.get('KEYS', 'api_secret')
            self.exchange.password = cfg.get('KEYS', 'api_passphrase')
        except Exception as e:
            self.logger.error("Cannot read exchange config file!" + str(e))

    def change_symbol_for_trade(self, symbol):
        if ":" in symbol:
            symbol = symbol.split(":")[0]
        if "-" in symbol:
            if "SWAP" in symbol:
                symbols = symbol.split("-")
                return symbols[0].upper() + "-" + symbols[1].upper()
            else:
                return symbol.upper()
        elif "_" in symbol:
            symbols = symbol.split("_")
            return symbols[0].upper() + "-" + symbols[1].upper()
        elif "/" in symbol:
            symbols = symbol.split("/")
            return symbols[0].upper() + "-" + symbols[1].upper()

    def change_symbol_for_data(self, symbol):
        if ":" in symbol:
            symbol = symbol.split(":")[0]
        if "-" in symbol:
            if "SWAP" in symbol:
                symbols = symbol.split("-")
                return symbols[0].upper() + "-" + symbols[1].upper()
            else:
                return symbol.upper() 
        elif "_" in symbol:
            symbols = symbol.split("_")
            return symbols[0].upper() + "-" + symbols[1].upper()
        elif "/" in symbol:
            symbols = symbol.split("/")
            return symbols[0].upper() + "-" + symbols[1].upper()

    def change_symbol_for_markets(self, symbol):
        if ":" in symbol:
            symbol = symbol.split(":")[0]
        if "-" in symbol:
            symbols = symbol.split("-")
            return symbols[0].upper() + "/" + symbols[1].upper()
        elif "_" in symbol:
            symbols = symbol.split("_")
            return symbols[0].upper() + "/" + symbols[1].upper()
        elif "/" in symbol:
            symbols = symbol.split("/")
            return symbols[0].upper() + "-" + symbols[1].upper()

    def get_contract_size(self, markets, pair):
        try:
            ePair = self.change_symbol_for_markets(pair) #Utility.get_exchange_format(pair+":USDT")
            for i in markets:
                if ePair in i:
                    ePair = i
                    break
            marketData = markets[ePair]
            if marketData['info']['minSz']:
                return marketData['info']['minSz']
            else:
                self.logger.error(f"Cannot find contractSize of {ePair}!")
                raise ValueError(f'Cannot find contractSize of {ePair}!')
        except Exception as e:
            self.logger.error(f"Cannot get contract size of {ePair}" + str(e))
        


