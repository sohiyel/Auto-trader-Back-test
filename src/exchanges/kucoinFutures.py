from src.exchanges.baseExchange import BaseExchange
import asyncio
import ccxt
from math import floor
from src.utility import Utility
from datetime import datetime
import time
from src.logManager import LogService

class KucoinFutures(BaseExchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        self.baseUrl = 'https://api-futures.kucoin.com/'
        self.exchange = ccxt.kucoinfutures()
        self.exchange.set_sandbox_mode(sandBox)
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        
    def fetch_balance(self):
        try:
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

    def get_klines(self, symbol, timeFrame, startAt, endAt):
        pts = {'pair': symbol, 'timeFrame': timeFrame, 'strategyName': 'NaN'}
        self.logService.set_pts_formatter(pts)
        symbol = self.exchange.change_symbol_for_trade(self.pair)
        timeFrame = Utility.unify_timeframe(timeFrame, "kucoinfutures")
        self.logger.info('requesting data for {} in timeframe {} from {} to {}'.format(symbol,timeFrame, str(datetime.fromtimestamp(startAt)), str(datetime.fromtimestamp(endAt))))
        status = True
        while status:
            response = self.exchange.fetch_ohlcv(symbol, timeFrame, startAt)
            if len(response) == 0:
                self.logger.error('Something went wrong. Error: respones is empty sleeping ... ')
                time.sleep(10)
            else: 
                self.logger.info('Success! recieved {} candles'.format(len(response)))
                return(response)

    async def get_klines_data(self, symbol, timeFrame, startAt, endAt, limit):
        klines = []
        startAt = startAt * 1000
        endAt = endAt * 1000
        timeFrame = Utility.unify_timeframe(timeFrame, "kucoinfutures")
        step = limit * Utility.array[timeFrame]
        for i in range(startAt,endAt,step):
            temp = []
            if (i+step < endAt):
                temp.extend(self.get_klines(symbol, timeFrame, i, i+step))
            else:
                temp.extend(self.get_klines(symbol, timeFrame, i, endAt))
            if temp:
                if len(temp) > 0:
                    klines.extend(temp)
                    await asyncio.sleep(2.5)
            else:
                self.logger.warning("The data is null!")
                break

        return klines

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