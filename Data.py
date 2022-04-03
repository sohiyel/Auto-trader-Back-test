from datetime import datetime
from pytz import timezone
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
        self.startAtTs = self.convert_time(startTime)
        self.endAtTs = self.convert_time(endTime)
        self.historyNeeded = int(historyNeeded)
        self.state = 0
        if market == 'futures':
            self.limit = 200
            self.client = KucoinFutures()
        else:
            self.limit = 1440
            self.client = KucoinSpot()
        
        asyncio.run(self.fetch_klines())

    def convert_time(self, ttime):
        date_time_obj = datetime.strptime(ttime, '%Y-%m-%d %H:%M:%S')
        utc_time = date_time_obj.replace(tzinfo=timezone('utc'))
        return int(datetime.timestamp(utc_time))

    async def fetch_klines(self):
        fileName = "./data/"+self.market+"/"+self.symbol+"_"+str(self.startAtTs - self.historyNeeded)+"_"+str(self.endAtTs)+".csv"
        if ( os.path.exists(fileName)):
            self.dataFrame = pd.read_csv(fileName)
            print(fileName + " has been read from disk")
        else:
            await self.get_klines()
        
    async def get_klines(self):
        print(self.startAtTs, self.endAtTs)
        limit = 1440 * tfMap.array[self.timeFrame] * 60
        self.klines = await self.client.get_klines_data(self.symbol, self.timeFrame, self.startAtTs - self.historyNeeded, self.endAtTs, limit)
        self.make_data_frame()
                        
    def make_data_frame(self):
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
        asyncio.create_task(self.write_to_CSV())
        
    async def write_to_CSV(self):
        fileName = "./data/"+self.market+"/"+self.symbol+"_"+str(self.startAtTs - self.historyNeeded)+"_"+str(self.endAtTs)+".csv"
        if ( os.path.exists(fileName)):
            return
        else:
            self.dataFrame.to_csv(fileName)
            self.dataFrame = pd.read_csv(fileName)
            print(fileName + " has been read from disk")


    def get_current_data(self, lastState):
        if lastState <= self.endAtTs:
            # print(lastState,  self.convertTime(self.dataFrame.iloc[0]["timestamp"]))
            dt_object = datetime.fromtimestamp(lastState, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
            # print(dt_object, self.dataFrame.iloc[0]["timestamp"])
            return self.dataFrame.loc[self.dataFrame['timestamp'] == dt_object]
        else:
            "<----------End of this dataset!---------->"
            return False

    # def read_data_from_db(self):
