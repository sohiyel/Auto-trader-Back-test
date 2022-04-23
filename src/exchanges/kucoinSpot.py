from src.exchanges.kucoin import Kucoin
import requests
import asyncio
import configparser
import ccxt as ccxt

class KucoinSpot(Kucoin):
    def __init__(self, settings, sandBox = False):
        super().__init__(sandBox)
        self.settings = settings
        self.baseUrl = 'https://api.kucoin.com'
        self.exchange = ccxt.kucoin()
        self.exchange.set_sandbox_mode(sandBox)

    def authorize(self):
        cfg = configparser.ConfigParser()
        if self.sandBox:
            cfg.read(self.settings.API_SANDBOX_PATH)
        else:
            cfg.read(self.settings.API_PATH)
        self.exchange.apiKey = cfg.get('KEYS','api_key')
        self.exchange.secret = cfg.get('KEYS', 'api_secret')
        self.exchange.password = cfg.get('KEYS', 'api_passphrase')

    def get_klines(self, symbol, timeFrame, startAt, endAt):
        kLineURL = '/api/v1/market/candles?'
        params = {
            'type': timeFrame,
            'symbol': symbol,
            'startAt': startAt,
            'endAt': endAt
        }
        print(params)
        response = requests.get(self.baseUrl+kLineURL,params=params)
        if response.status_code ==  200:
            print(response.json())
            return(response.json()['data'])
        else:
            print("Something went wrong. Error: "+ str(response.status_code))

    async def get_klines_data(self, symbol, timeFrame, startAt, endAt, limit):
        klines = []
        for i in range(startAt,endAt,limit):
            temp = []
            if (i+limit < endAt):
                temp.extend(self.get_klines(symbol, timeFrame, i, i+limit))
            else:
                temp.extend(self.get_klines(symbol, timeFrame, i, endAt))
            if temp:
                if len(temp) > 0:
                    klines.extend(temp)
                    print(temp[0][0],temp[-1][0])
                    await asyncio.sleep(5)
            else:
                break

        return klines