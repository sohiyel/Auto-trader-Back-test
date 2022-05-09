from datetime import datetime
from psycopg2 import Timestamp
from pytz import timezone
import os
import asyncio
import pandas as pd
from pytz import timezone
from src.exchanges.kucoinFutures import KucoinFutures
from src.exchanges.kucoinSpot import KucoinSpot
from src.tfMap import tfMap
from src.databaseManager import DatabaseManager
from os import path
class DataService():

    def __init__(self, market, pair, timeFrame, startTime, endTime, historyNeeded = 0, settings=''):
        self.pair = pair
        self.settings = settings
        self.dbPair = tfMap.get_db_format(self.pair)
        self.timeFrame = timeFrame
        self.tableName = self.dbPair + "_" + self.timeFrame
        self.startTime = startTime
        self.endTime = endTime
        self.klines = []
        self.dataFrame = ""
        self.market = market
        self.startAtTs = self.convert_time(startTime)
        self.endAtTs = self.convert_time(endTime)
        self.historyNeeded = int(historyNeeded)
        self.state = 0
        self.db = DatabaseManager(settings)
        if market == 'futures':
            self.limit = self.settings.constantNumbers["data_limit_future"]
            self.client = KucoinFutures(settings)
        else:
            self.limit = self.settings.constantNumbers["data_limit_spot"]
            self.client = KucoinSpot(settings)
        
        self.fetch_klines()

    def convert_time(self, ttime):
        date_time_obj = datetime.strptime(ttime, '%Y-%m-%d_%H:%M:%S')
        utc_time = date_time_obj.replace(tzinfo=timezone('utc'))
        return int(datetime.timestamp(utc_time))

    # async def fetch_klines(self):
    #     fileName = path.join(self.settings.DATA_DIR,self.market,self.dbPair+"_"+str(self.startAtTs - self.historyNeeded)+"_"+str(self.endAtTs)+".csv")
    #     if ( os.path.exists(fileName)):
    #         self.dataFrame = pd.read_csv(fileName)
    #         print(fileName + " has been read from disk")
    #     else:
    #         await self.get_klines()

    def fetch_klines(self):
        self.dataFrame = self.db.fetch_klines(self.pair, self.timeFrame, (self.startAtTs - self.historyNeeded) * 1000, self.endAtTs * 1000)
        print(" Expected candles:", (self.endAtTs - (self.startAtTs - self.historyNeeded))/(tfMap.array[self.timeFrame]*60))
        print( "Existing candles:", self.dataFrame.shape[0])
        print("Needed start and end time:", (self.startAtTs - self.historyNeeded)*1000, self.endAtTs*1000)
        print("Existed start anad end time:", self.dataFrame.iloc[-1]['timestamp'], self.dataFrame.iloc[0]['timestamp'])
        
    async def get_klines(self):
        #print(self.startAtTs, self.endAtTs)
        limit = 1440 * tfMap.array[self.timeFrame] * 60
        self.klines = await self.client.get_klines_data(self.pair, self.timeFrame, self.startAtTs - self.historyNeeded, self.endAtTs, limit)
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
        
        self.db.create_ohlcv_table(self.dbPair, self.timeFrame)
        self.db.store_klines(dataFrame, self.tableName)
        #dataFrame['timestamp'] = pd.to_datetime(dataFrame['timestamp'], unit='ms')
        dataFrame.set_index('timestamp', inplace=True)
        dataFrame.sort_index(inplace=True)
        self.dataFrame = dataFrame
        asyncio.create_task(self.write_to_CSV())
        
    async def write_to_CSV(self):
        fileName = path.join(self.settings.DATA_DIR,self.market,self.dbPair+"_"+str(self.startAtTs - self.historyNeeded)+"_"+str(self.endAtTs)+".csv")
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

    def read_data_from_db(self, limit, lastState):
        return self.db.read_klines(self.dbPair, self.timeFrame, limit, lastState)

    def read_data_from_memory(self, limit, lastState):
        candles = self.dataFrame.loc[self.dataFrame['timestamp'] <= lastState]
        return candles.tail(limit)
        
        d1 = d1.sort_values(by='timestamp', ascending=True)
        d2 = self.db.read_klines(self.dbPair, self.timeFrame, limit, lastState)
        d1.to_csv("d1.csv")
        d2.to_csv("d2.csv")
        return d1

