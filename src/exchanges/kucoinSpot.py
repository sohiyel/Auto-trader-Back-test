from src.exchanges.baseExchange import BaseExchange
import ccxt as ccxt
from src.logManager import LogService
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

    def fetch_balance(self):
        response = self.exchange.fetch_accounts()
        for i in response:
            if i['type'] == 'trade':
                return {'Balance': i['info']['balance'],
                        'Equity': i['info']['available']}
        return

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