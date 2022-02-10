from kucoin import Kucoin
import requests
import asyncio

class KucoinSpot(Kucoin):
    def __init__(self, market):
        super().__init__(market)
        self.baseUrl = 'https://api.kucoin.com'
        self.limit = 1440 * 60

    def get_klines(self, symbol, timeFrame, startAt, endAt):
        kLineURL = '/api/v1/market/candles?'
        params = {
            'type': timeFrame,
            'symbol': symbol,
            'startAt': startAt,
            'endAt': endAt
        }
        response = requests.get(self.baseUrl+kLineURL,params=params)
        if response.status_code ==  200:
            return(response.json()['data'])
        else:
            print("Something went wrong. Error: "+ str(response.status_code))

    async def get_klines_data(self, symbol, timeFrame, startAt, endAt):
        klines = []
        for i in range(startAt,endAt,self.limit):
            temp = []
            if (i+self.limit < endAt):
                temp.extend(self.get_klines(symbol, timeFrame, i, i+self.limit))
            else:
                temp.extend(self.get_klines(symbol, timeFrame, i, endAt))
            if temp:
                if len(temp) > 0:
                    klines.extend(temp)
                    print(temp[0][0],temp[-1][0])
                    await asyncio.sleep(2.5)
            else:
                break

        return klines