from datetime import datetime
import os
from kucoin.client import Client
import asyncio
import pandas as pd
import configparser


cfg = configparser.ConfigParser()
cfg.read('api.cfg')
api_key = cfg.get('KEYS','api_key')
api_secret = cfg.get('KEYS', 'api_secret')
api_passphrase = cfg.get('KEYS', 'api_passphrase')
client = Client(api_key, api_secret, api_passphrase)

class DataService():

    def __init__(self, symbol, timeFrame, startTime, endTime, limit=1440*60):
        self.symbol = symbol
        self.timeFrame = timeFrame
        self.startTime = startTime
        self.endTime = endTime
        self.klines = []
        self.limit = limit
        self.dataFrame = ""
        
        asyncio.run(self.fetchKlines())

    def convertTime(self, ttime):
        date_time_obj = datetime.strptime(ttime, '%Y-%m-%d')
        return datetime.timestamp(date_time_obj)

    async def fetchKlines(self):
        fileName = "./data/"+self.symbol+"_"+self.startTime+"_"+self.endTime+".csv"
        if ( os.path.exists(fileName)):
            self.dataFrame = pd.read_csv(fileName)
            print(fileName + " has been read from disk")
        else:
            await self.getKlines()
        
    async def getKlines(self):
        startTime = int(self.convertTime(self.startTime))
        endTime = int(self.convertTime(self.endTime))
        print(startTime, endTime)
        for i in range(startTime,endTime,self.limit):
            temp = []
            if (i+self.limit < endTime):
                temp.extend(client.get_kline_data(self.symbol, self.timeFrame, i, i+self.limit))
            else:
                temp.extend(client.get_kline_data(self.symbol, self.timeFrame, i, endTime))
            self.klines.extend(temp)
            print(temp[0][0],temp[-1][0])
            await asyncio.sleep(2.5)
        self.makeDataFrame()
                        
    def makeDataFrame(self):
        dataFrame = pd.DataFrame(self.klines, columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume', 'amount'])
        dataFrame['timestamp'] = dataFrame['timestamp'].astype(float)*1000
        dataFrame['timestamp'] = pd.to_datetime(dataFrame['timestamp'], unit='ms')
        dataFrame.set_index('timestamp', inplace=True)
        self.dataFrame = dataFrame
        asyncio.create_task(self.writeToCSV())
        
    async def writeToCSV(self):
        fileName = "./data/"+self.symbol+"_"+self.startTime+"_"+self.endTime+".csv"
        if ( os.path.exists(fileName)):
            return
        else:
            self.dataFrame.to_csv(fileName)




    
d = DataService("BTC-USDT", "1min", "2021-01-01", "2021-01-03")