from turtle import position
from src.exchanges.baseExchange import BaseExchange
import ccxt
from math import floor
from src.logManager import LogService
import time
from src.exchangePosition import ExchangePosition

class KucoinFutures(BaseExchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        self.baseUrl = 'https://api-futures.kucoin.com/'
        self.exchange = ccxt.kucoinfutures()
        self.exchange.set_sandbox_mode(sandBox)
        self.exchange.enableRateLimit = True
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        
    def fetch_balance(self):
        try:
            self.logger.critical("API request: Fetch Balance")
            response = self.exchange.fetch_balance(params={"currency":"USDT"})
            if response['info']['code'] == '200000':
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

    def change_symbol_for_trade(self, symbol):
        if "/" in symbol:
            if ":" in symbol:
                return symbol.upper()
            else:
                return symbol.upper() + ":USDT"
        elif "_" in symbol:
            symbols = symbol.split("_")
            return symbols[0].upper() + "/" + symbols[1].upper() + ":USDT"
        elif "-" in symbol:
            symbols = symbol.split("-")
            return symbols[0].upper() + "/" + symbols[1].upper() + ":USDT"

    def change_symbol_for_data(self, symbol):
        return self.change_symbol_for_trade(symbol)

    def change_symbol_for_markets(self, symbol):
        return self.change_symbol_for_data(symbol)

    def lot_calculator(self, symbol, amount):
        """
        this function is written for calculate lot size of kucoin future
        :param exchange:
        :param symbol:
        :param amount:
        :return: size in lot
        """
        data = self.exchange.futuresPublicGetContractsSymbol({
            'symbol': symbol
        })
        min_lot = float(data['data']['multiplier'])
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
        exchangePositions = self.exchange.fetch_positions()
        self.logger.critical("API request: Fetch Positions")
        positions = []
        for p in exchangePositions:
            positions.append(ExchangePosition(p["symbol"], p["side"], p["contracts"] , p["contractSize"], p["leverage"]))
        return positions

    def close_positions(self, pair = ""):
        exchangePositions = self.fetch_positions()
        self.logger.debug(exchangePositions)
        for i in exchangePositions:
            if pair:
                if not i.pair == pair:
                    continue
            done = True
            attempt = 0
            while done and attempt < 3:
                if i.side == "long":
                    try:
                        self.exchange.create_market_order(i.pair, "sell", i.contracts, i.leverage, params={'leverage': i.leverage})
                        self.logger.critical("API request: Create market order")
                        self.logger.info( f"-------- Close buy position on {i.pair}--------")
                        time.sleep(1)
                        done = False
                    except Exception as e:
                        self.logger.error("Cannot create market order!" + str(e))
                        time.sleep(10)
                        attempt += 1
                elif i.side == "short":
                    try:
                        self.exchange.create_market_order(i.pair, "buy", i.contracts,i.leverage, params={'leverage': i.leverage})
                        self.logger.critical("API request: Create market order")
                        self.logger.info( f"-------- Close sell position on {i.pair}--------")
                        time.sleep(1)
                        done = False
                    except Exception as e:
                        self.logger.error("Cannot create market order!" + str(e))
                        time.sleep(10)
                        attempt += 1

    def get_second_currency(self, symbol):
        symbols = symbol.split("/")
        return symbols[1].split(":")[0]

    def get_first_currency(self, symbol):
        symbols = symbol.split("/")
        return symbols[0]