from urllib import response
from src.exchanges.baseExchange import BaseExchange
import ccxt as ccxt
from src.logManager import LogService
from src.markets import Markets
import math
from src.utility import Utility
class KucoinSpot(BaseExchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        self.baseUrl = 'https://api.kucoin.com'
        self.exchange = ccxt.kucoin()
        self.exchange.set_sandbox_mode(sandBox)
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger

    def change_symbol_for_trade(self, symbol):
        if "/" in symbol:
            if ":" in symbol:
                symbols = symbol.split(":")
                return symbols[0].upper()
            else:
                return symbol.upper()
        elif "_" in symbol:
            symbols = symbol.split("_")
            return symbols[0].upper() + "/" + symbols[1].upper()
        elif "-" in symbol:
            symbols = symbol.split("-")
            return symbols[0].upper() + "/" + symbols[1].upper()

    def change_symbol_for_data(self, symbol):
        return self.change_symbol_for_trade(symbol)

    def change_symbol_for_markets(self, symbol):
        return self.change_symbol_for_data(symbol)

    def fetch_balance(self, symbol=""):
        response = self.exchange.fetch_accounts()
        self.logger.debug(response)
        if symbol:
            currency = self.get_second_currency(symbol)
            for i in response:
                if i['type'] == 'trade' and i['currency'] == currency:
                    roundNumber = int(abs(math.log10(Markets(self.settings).get_contract_size(symbol)) ))
                    return {'Balance': Utility.truncate(float(i['info']['balance']),roundNumber),
                            'Equity': Utility.truncate(float(i['info']['available']),roundNumber)}
        else:
            currency = self.settings.baseCurrency
            for i in response:
                if i['type'] == 'trade' and i['currency'] == currency:
                    return {'Balance': float(i['info']['balance']),
                            'Equity': float(i['info']['available'])}
        return {'Balance': 0,
                'Equity': 0}

    def fetch_accounts(self):
        wallet = {}
        try:
            response = self.exchange.fetch_accounts()
            for i in response:
                if i['type'] == 'trade':
                    if not i['currency'] == self.settings.baseCurrency:
                        wallet[i['currency']] = i['info']['balance']
            return wallet
        except Exception as e:
            self.logger.error("Cannot fetch accounts!")
            return wallet

    def get_contract_size(self, markets, pair):
        try:
            ePair = self.change_symbol_for_markets(pair) #Utility.get_exchange_format(pair+":USDT")
            for i in markets:
                if ePair in i:
                    ePair = i
                    break
            marketData = markets[ePair]
            if marketData['info']['baseMinSize']:
                return marketData['info']['baseMinSize']
            else:
                self.logger.error(f"Cannot find contractSize of {ePair}!")
                raise ValueError(f'Cannot find contractSize of {ePair}!')
        except Exception as e:
            self.logger.error(f"Cannot get contract size of {ePair}" + str(e))

    def get_second_currency(self, symbol):
        symbols = symbol.split("/")
        return symbols[1]

    def get_first_currency(self, symbol):
        symbols = symbol.split("/")
        return symbols[0]