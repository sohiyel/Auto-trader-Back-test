from kucoin import Kucoin
import requests
import asyncio
import ccxt
import configparser

from tfMap import tfMap

class KucoinFutures(Kucoin):
    def __init__(self, sandBox = False):
        super().__init__(sandBox)
        self.baseUrl = 'https://api-futures.kucoin.com/'
        self.exchange = ccxt.kucoinfutures()
        self.exchange.set_sandbox_mode(sandBox)

    def authorize(self):
        cfg = configparser.ConfigParser()
        if self.sandBox:
            cfg.read('api_sandbox_future.cfg')
        else:
            cfg.read('configurations/api_future.cfg')
        self.exchange.apiKey = cfg.get('KEYS','api_key')
        self.exchange.secret = cfg.get('KEYS', 'api_secret')
        self.exchange.password = cfg.get('KEYS', 'api_passphrase')
        # print( self.exchange.fetch_balance())

    def get_klines(self, symbol, timeFrame, startAt, endAt):
        return self.exchange.fetch_ohlcv(symbol, timeFrame, startAt)
        # kLineURL = 'api/v1/kline/query?'
        # params = {
        #     'symbol': symbol,
        #     'granularity': granularity,
        #     'from': startAt,
        #     'to': endAt
        # }
        # print(self.baseUrl+kLineURL,params)
        # response = requests.get(self.baseUrl+kLineURL,params=params)
        # if response.status_code ==  200:
        #     return(response.json()['data'])
        # else:
        #     print("Something went wrong. Error: "+ str(response.status_code))

    async def get_klines_data(self, symbol, timeFrame, startAt, endAt, limit):
        klines = []
        startAt = startAt * 1000
        endAt = endAt * 1000
        step = limit * tfMap.array[timeFrame]
        print(startAt, endAt, step)
        for i in range(startAt,endAt,step):
            temp = []
            if (i+step < endAt):
                temp.extend(self.get_klines(symbol, timeFrame, i, i+step))
            else:
                temp.extend(self.get_klines(symbol, timeFrame, i, endAt))
            if temp:
                if len(temp) > 0:
                    klines.extend(temp)
                    print(temp[0][0],temp[-1][0])
                    await asyncio.sleep(2.5)
            else:
                print("The data is null!")
                break

        return klines