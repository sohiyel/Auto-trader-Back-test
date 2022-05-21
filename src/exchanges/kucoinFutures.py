from src.exchanges.kucoin import Kucoin
import requests
import asyncio
import ccxt
import configparser
from src.utility import Utility
from datetime import datetime
import time
from src.logManager import get_logger

class KucoinFutures(Kucoin):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        super().__init__(sandBox)
        self.baseUrl = 'https://api-futures.kucoin.com/'
        self.exchange = ccxt.kucoinfutures()
        self.exchange.set_sandbox_mode(sandBox)
        self.logger = get_logger(__name__, settings)

    def authorize(self):
        cfg = configparser.ConfigParser()
        try:
            if self.sandBox:
                cfg.read(self.settings.API_SANDBOX_FUTURE_PATH)
            else:
                cfg.read(self.settings.API_FUTURE_PATH)
            self.exchange.apiKey = cfg.get('KEYS','api_key')
            self.exchange.secret = cfg.get('KEYS', 'api_secret')
            self.exchange.password = cfg.get('KEYS', 'api_passphrase')
        except:
            self.logger.error("Cannot read exchange config file!")

    def get_klines(self, symbol, timeFrame, startAt, endAt):
        symbol = Utility.get_exchange_format(symbol)
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
        # kLineURL = 'api/v1/kline/query?'
        # params = {
        #     'symbol': symbol,
        #     'granularity': granularity,
        #     'from': startAt,
        #     'to': endAt
        # }
        # response = requests.get(self.baseUrl+kLineURL,params=params)
        # if response.status_code ==  200:
        #     return(response.json()['data'])
        # else:
        #     self.logger.error("Something went wrong. Error: "+ str(response.status_code))

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