import ccxt
from src.databaseManager import DatabaseManager
from src.utility import Utility
from datetime import datetime
from pytz import timezone
import pandas as pd
import time
import concurrent.futures
import json
from src.settings import Settings
import sys
import os
from src.data import DataService

class DataDownloader():
    def __init__(self, pair, timeFrame, settings) -> None:
        self.settings = settings
        self.pair = pair
        self.timeFrame = Utility.unify_timeframe(timeFrame, settings.exchange)
        pair = Utility.get_db_format(self.pair)
        self.tableName = pair + "_" + self.timeFrame
        self.exchange = ccxt.kucoinfutures()
        self.db = DatabaseManager(settings)

    def get_klines(self):
        pair = Utility.get_exchange_format(self.pair)
        klines = self.exchange.fetch_ohlcv(pair, self.timeFrame)
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df

    def fetch_klines(self, startAt, endAt):
        pair = Utility.get_exchange_format(self.pair)
        klinesList = []
        lastDate = startAt
        while lastDate < endAt+1:
            klines = self.exchange.fetch_ohlcv(pair, self.timeFrame, lastDate)
            if len(klines) == 0:
                print('        Something went wrong in getting klines sleeping ... ')
                time.sleep(10)
            else:
                print('        Success! recieved {} candles'.format(len(klines)))
                lastDate = klines[-1][0]
                klinesList.extend(klines)
                df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                self.db.store_klines(df, self.tableName)
                time.sleep(3)
        print('        Expected {} candles!'.format((endAt - startAt)/(Utility.array[self.timeFrame]*60000)))
        print('        Done! recieved {} candles'.format(len(klinesList)))
        firstDate = datetime.fromtimestamp(klinesList[0][0]/1000, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
        endDate = datetime.fromtimestamp(klinesList[-1][0]/1000, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
        print(f'        From {firstDate} to {endDate}')

    def find_new_data(self, klines):
        df = self.db.read_klines(self.pair, self.timeFrame, 200, time.time())
        diff = klines.merge(df, how = 'outer', indicator = True).loc[ lambda x : x['_merge'] == 'left_only']
        return diff

    def main_loop(self):
        while True:
            klines = self.get_klines()
            self.db.create_ohlcv_table(self.pair,self.timeFrame)
            diff = self.find_new_data(klines)
            self.db.store_klines(diff,self.tableName)
            print (f"{diff.shape[0]} new canldes were added to {self.tableName}")
            time.sleep(Utility.array[self.timeFrame] * 60)

class Downloader():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.tablesList = self.find_tables()
        self.indexes = []

    def initialize_indexes(self, table):
        downloader = DataDownloader(table[0], table[1], self.settings)
        downloader.main_loop()
        self.indexes.append(downloader)
        print  (f"--------- Initialized :{table[0]} _ {table[1]} ---------")
        time.sleep(1)

    def find_tables(self):
        tables = []
        with open(self.settings.DATABASE_INDEXES_PATH,"r") as json_data_file:
            jsonFile = json.load(json_data_file)
            ptss = jsonFile["tables"]
            for pts in ptss:
                tables.append( (pts["pair"], pts["tf"]))
        return tables

if __name__ == '__main__':
    settings = Settings(sys.argv[1])
    if os.path.exists(settings.ACCOUNT_DIR):
        downloader = Downloader(settings)
        with concurrent.futures.ThreadPoolExecutor() as executor:        
            executor.map(downloader.initialize_indexes,downloader.tablesList)

