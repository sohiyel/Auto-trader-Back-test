from datetime import datetime, timezone
import os
import asyncio
import pandas as pd
from pytz import timezone
from kucoinFutures import KucoinFutures
from kucoinSpot import KucoinSpot
from tfMap import tfMap

class DataService():

    def __init__(self, market, symbol, timeFrame, startTime, endTime, historyNeeded = 0):
        self.symbol = symbol
        self.timeFrame = timeFrame
        self.startTime = startTime
        self.endTime = endTime
        self.klines = []
        self.dataFrame = ""
        self.market = market
        self.startAtTs = self.convertTime(startTime)
        self.endAtTs = self.convertTime(endTime)
        self.historyNeeded = int(historyNeeded)
        self.state = 0
        if market == 'futures':
            self.limit = 200
            self.client = KucoinFutures(market, timeFrame)
        else:
            self.limit = 1440
            self.client = KucoinSpot(market, timeFrame)
        
        asyncio.run(self.fetchKlines())

    def convertTime(self, ttime):
        date_time_obj = datetime.strptime(ttime, '%Y-%m-%d %H:%M:%S')
        utc_time = date_time_obj.replace(tzinfo=timezone('utc'))
        return int(datetime.timestamp(utc_time))

    async def fetchKlines(self):
        fileName = "./data/"+self.market+"/"+self.symbol+"_"+str(self.startAtTs - self.historyNeeded)+"_"+str(self.endAtTs)+".csv"
        if ( os.path.exists(fileName)):
            self.dataFrame = pd.read_csv(fileName)
            print(fileName + " has been read from disk")
        else:
            await self.getKlines()
        
    async def getKlines(self):
        print(self.startAtTs, self.endAtTs)
        self.klines = await self.client.get_klines_data(self.symbol, self.timeFrame, self.startAtTs - self.historyNeeded, self.endAtTs)
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
        fileName = "./data/"+self.market+"/"+self.symbol+"_"+str(self.startAtTs - self.historyNeeded)+"_"+str(self.endAtTs)+".csv"
        if ( os.path.exists(fileName)):
            return
        else:
            self.dataFrame.to_csv(fileName)
            self.dataFrame = pd.read_csv(fileName)
            print(fileName + " has been read from disk")


    def getCurrentData(self, lastState):
        if lastState <= self.endAtTs:
            # print(lastState,  self.convertTime(self.dataFrame.iloc[0]["timestamp"]))
            dt_object = datetime.fromtimestamp(lastState, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
            # print(dt_object, self.dataFrame.iloc[0]["timestamp"])
            return self.dataFrame.loc[self.dataFrame['timestamp'] == dt_object]
        else:
            "<----------End of this dataset!---------->"
            return False