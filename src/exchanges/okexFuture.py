from src.exchanges.baseExchange import BaseExchange
import ccxt
from src.logManager import LogService
import configparser
from math import floor
import time
from src.exchangePosition import ExchangePosition

class OkexFuture(BaseExchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        self.exchange = ccxt.okex5()
        self.exchange.options['createMarketBuyOrderRequiresPrice'] = False
        self.exchange.options['defaultType'] = 'future'
        self.exchange.set_sandbox_mode(sandBox)
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
    
    def fetch_balance(self):
        currency = self.settings.baseCurrency
        try:
            response = self.exchange.fetch_balance()
            self.logger.debug("Fetch balance response: ", response)
            if response['info']['code'] == '0':
                try:
                    return {
                        'Equity' : float(response[currency]['free']),
                        'Balance' : float(response[currency]['total'])
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

    def create_market_order(self, symbol, side, amount, leverage = 1, comment="", price=None, params={}):
        pts = {'pair': symbol, 'timeFrame': 'NaN', 'strategyName': 'NaN'}
        self.logService.set_pts_formatter(pts)
        self.logger.debug("Volume: "+ str(amount))
        if comment == 'open_buy':
            self.exchange.set_leverage(leverage,symbol,params={'mgnMode': 'isolated','posSide': 'long'})
            okexParams={'tdMode': 'isolated', 'posSide': 'long'}
        elif comment == 'open_sell':
            self.exchange.set_leverage(leverage,symbol,params={'mgnMode': 'isolated','posSide': 'short'})
            okexParams={'tdMode': 'isolated', 'posSide': 'short'}
        elif comment == 'close_buy':
            self.exchange.set_leverage(leverage,symbol,params={'mgnMode': 'isolated','posSide': 'long'})
            okexParams={'tdMode': 'isolated', 'posSide': 'long'}
        elif comment == 'close_sell':
            self.exchange.set_leverage(leverage,symbol,params={'mgnMode': 'isolated','posSide': 'short'})
            okexParams={'tdMode': 'isolated', 'posSide': 'short'}
        self.logger.debug("Create market order with params = ",okexParams)
        return self.exchange.create_market_order(symbol, side, amount, params=okexParams)

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
                return symbol.upper()
            else:
                return symbol.upper() + "-SWAP"
        elif "_" in symbol:
            symbols = symbol.split("_")
            return symbols[0].upper() + "-" + symbols[1].upper() + "-SWAP"
        elif "/" in symbol:
            symbols = symbol.split("/")
            return symbols[0].upper() + "-" + symbols[1].upper() + "-SWAP"

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
            return symbols[0].upper() + "/" + symbols[1].upper() + ":USDT"
        elif "_" in symbol:
            symbols = symbol.split("_")
            return symbols[0].upper() + "/" + symbols[1].upper() + ":USDT"
        elif "/" in symbol:
            symbols = symbol.split("/")
            return symbols[0].upper() + "-" + symbols[1].upper() + ":USDT"

    def lot_calculator(self, symbol, amount):
        """
        this function is written for calculate amount size in lot (OKEx SWAP contacts)
        :param amount:
        :param exchange:
        :param symbol:
        :return: size in lot
        """

        data = self.exchange.fetch_markets_by_type(type='SWAP', params={
            'instId': symbol
        })
        min_lot = float(data[0]['info']['ctVal'])
        size = floor(amount / min_lot) if amount > min_lot else 1
        return size
        
    def get_contract_size(self, markets, pair):
        try:
            ePair = self.change_symbol_for_markets(pair) #Utility.get_exchange_format(pair+":USDT")
            for i in markets:
                if ePair in i:
                    self.logger.debug(i)
                    ePair = i
                    break
            marketData = markets[ePair]
            if marketData['contractSize']:
                return marketData['contractSize']
            else:
                self.logger.error(f"Cannot find contractSize of {ePair}!")
                raise ValueError(f'Cannot find contractSize of {ePair}!')
        except Exception as e:
            self.logger.error(f"Cannot get contract size of {ePair}" + str(e))

    def fetch_positions(self):
        try:
            exchangePositions = self.exchange.privateGetAccountPositions()['data']
            self.logger.debug(exchangePositions)
            positions = []
            for p in exchangePositions:
                positions.append(ExchangePosition(p["instId"], p["posSide"], p["availPos"] , 1, p["lever"]))
            return positions
        except Exception as e:
            self.logger.error("Cannot get positions! "+str(e))
            return False

    def close_positions(self, pair=""):
        positions = self.fetch_positions()
        if positions:
            try:
                for p in positions:
                    if pair:
                        if not pair == p.pair:
                            continue
                    self.exchange.private_post_trade_close_position(params={'instId': p.pair,'mgnMode': 'isolated','posSide': p.side})
                    time.sleep(1)
            except Exception as e:
                self.logger.error("Cannot close positions! " + str(e))

    def get_second_currency(self, symbol):
        symbols = symbol.split("-")
        return symbols[1]

    def get_first_currency(self, symbol):
        symbols = symbol.split("-")
        return symbols[0]


