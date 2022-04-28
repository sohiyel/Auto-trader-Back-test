import ccxt
from src.databaseManager import DatabaseManager
from src.tfMap import tfMap
from datetime import datetime
from pytz import timezone
import pandas as pd
import time
import concurrent.futures
import json
from src.settings import Settings
import sys
import os

class DataDownloader():
    def __init__(self, pair, timeFrame, settings) -> None:
        self.settings = settings
        self.pair = pair
        self.timeFrame = timeFrame
        pair = tfMap.get_db_format(self.pair)
        self.tableName = pair + "_" + self.timeFrame
        self.exchange = ccxt.kucoinfutures()
        self.db = DatabaseManager(settings)

    def get_klines(self):
        pair = tfMap.get_exchange_format(self.pair)
        klines = self.exchange.fetch_ohlcv(pair, self.timeFrame)
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df

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
            time.sleep(tfMap.array[self.timeFrame] * 60)

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
