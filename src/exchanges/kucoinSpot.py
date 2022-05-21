from src.exchanges.kucoin import Kucoin
import requests
import asyncio
import configparser
import ccxt as ccxt
from datetime import datetime
from time import sleep
from src.utility import Utility
from src.logManager import get_logger
class KucoinSpot(Kucoin):
    def __init__(self, settings, sandBox = False):
        super().__init__(sandBox)
        self.settings = settings
        self.baseUrl = 'https://api.kucoin.com'
        self.exchange = ccxt.kucoin()
        self.exchange.set_sandbox_mode(sandBox)
        self.logger = get_logger(__name__, settings)

    def authorize(self):
        cfg = configparser.ConfigParser()
        try:
            if self.sandBox:
                cfg.read(self.settings.API_SANDBOX_PATH)
            else:
                cfg.read(self.settings.API_PATH)
            self.exchange.apiKey = cfg.get('KEYS','api_key')
            self.exchange.secret = cfg.get('KEYS', 'api_secret')
            self.exchange.password = cfg.get('KEYS', 'api_passphrase')
        except:
            self.logger.error("Cannot read exchange config file!")

    def get_klines(self, symbol, timeFrame, startAt, endAt):
        kLineURL = '/api/v1/market/candles?'
        timeFrame = Utility.unify_timeframe(timeFrame, "kucoin")
        params = {
            'type': timeFrame,
            'symbol': symbol,
            'startAt': startAt,
            'endAt': endAt
        }
        self.logger.info('requesting data for {} in timeframe {} from {} to {}'.format(symbol,timeFrame, str(datetime.fromtimestamp(startAt)), str(datetime.fromtimestamp(endAt))))
        status = True
        while status:
            response = requests.get(self.baseUrl+kLineURL,params=params)
            if response.status_code != 200:
                self.logger.error('Something went wrong. Error: {} sleeping ... '.format(response.status_code))
                sleep(10)
            else:
                
                self.logger.info('Success! recieved {} candles'.format(len(response.json()['data'])))
                return(response.json()['data'])

    async def get_klines_data(self, symbol, timeFrame, startAt, endAt, limit):
        klines = []
        timeFrame = Utility.unify_timeframe(timeFrame, "kucoin")
        for i in range(startAt,endAt,limit):
            temp = []
            if (i+limit < endAt):
                temp.extend(self.get_klines(symbol, timeFrame, i, i+limit))
            else:
                temp.extend(self.get_klines(symbol, timeFrame, i, endAt))
            if temp:
                if len(temp) > 0:
                    klines.extend(temp)
                    await asyncio.sleep(5)
            else:
                break

        return klines