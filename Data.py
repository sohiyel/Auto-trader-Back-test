from datetime import datetime, timezone
import os
import asyncio
import pandas as pd
from pytz import timezone
from kucoinFutures import KucoinFutures
from kucoinSpot import KucoinSpot

class DataService():

    def __init__(self, market, symbol, timeFrame, startTime, endTime):
        self.symbol = symbol
        self.timeFrame = timeFrame
        self.startTime = startTime
        self.endTime = endTime
        self.klines = []
        self.dataFrame = ""
        self.market = market
        if market == 'futures':
            self.limit = 200
            self.client = KucoinFutures(market)
        else:
            self.limit = 1440
            self.client = KucoinSpot(market)
        
        asyncio.run(self.fetchKlines())

    def convertTime(self, ttime):
        date_time_obj = datetime.strptime(ttime, '%Y-%m-%d')
        utc_time = date_time_obj.replace(tzinfo=timezone('utc'))
        return datetime.timestamp(utc_time)

    async def fetchKlines(self):
        fileName = "./data/"+self.market+"/"+self.symbol+"_"+self.startTime+"_"+self.endTime+".csv"
        if ( os.path.exists(fileName)):
            self.dataFrame = pd.read_csv(fileName)
            print(fileName + " has been read from disk")
        else:
            await self.getKlines()
        
    async def getKlines(self):
        startTime = int(self.convertTime(self.startTime))
        endTime = int(self.convertTime(self.endTime))
        print(startTime, endTime)
        self.klines = await self.client.get_klines_data(self.symbol, self.timeFrame, startTime, endTime)
        self.makeDataFrame()
                        
    def makeDataFrame(self):
        if self.market == "futures":
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            dataFrame = pd.DataFrame(self.klines, columns = columns)
            dataFrame['timestamp'] = dataFrame['timestamp'].astype(float)
        else:
            columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume', 'amount']
            dataFrame = pd.DataFrame(self.klines, columns = columns)
            dataFrame['timestamp'] = dataFrame['timestamp'].astype(float)*1000
        dataFrame['timestamp'] = pd.to_datetime(dataFrame['timestamp'], unit='ms')
        dataFrame.set_index('timestamp', inplace=True)
        dataFrame.sort_index(inplace=True)
        self.dataFrame = dataFrame
        asyncio.create_task(self.writeToCSV())
        
    async def writeToCSV(self):
        fileName = "./data/"+self.market+"/"+self.symbol+"_"+self.startTime+"_"+self.endTime+".csv"
        if ( os.path.exists(fileName)):
            return
        else:
            self.dataFrame.to_csv(fileName)