from src.exchanges.baseExchange import BaseExchange
import asyncio
import ccxt

from src.utility import Utility
from datetime import datetime
import time
from src.logManager import get_logger

class KucoinFutures(BaseExchange):
    def __init__(self, settings, sandBox = False):
        self.settings = settings
        self.baseUrl = 'https://api-futures.kucoin.com/'
        self.exchange = ccxt.kucoinfutures()
        self.exchange.set_sandbox_mode(sandBox)
        self.logger = get_logger(__name__, settings)
        self.authorize()
        
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