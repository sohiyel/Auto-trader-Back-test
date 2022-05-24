from src.exchanges.exchange import Exchange
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
from src.logManager import get_logger

class DataDownloader():
    def __init__(self, pair, timeFrame, settings) -> None:
        self.settings = settings
        self.pair = Utility.get_exchange_format(pair)
        self.timeFrame = Utility.unify_timeframe(timeFrame, settings.exchange)
        self.dbPair = Utility.get_db_format(self.pair)
        self.tableName = self.dbPair + "_" + self.timeFrame
        self.exchange = Exchange(settings).exchange
        self.db = DatabaseManager(settings)
        self.logger = get_logger(__name__, settings)

    def get_current_klines(self):
        try:
            klines = self.exchange.fetch_ohlcv(self.pair, self.timeFrame)
        except Exception as e:
            self.logger.error("Cannot fetch_ohlcv!" + str(e))
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df

    def fetch_klines(self, startAt, endAt):
        klinesList = []
        lastDate = startAt
        while lastDate < endAt+1:
            klines = self.exchange.fetch_ohlcv(self.pair, self.timeFrame, lastDate)
            if len(klines) == 0:
                self.logger.warning('Something went wrong in getting klines sleeping ... ')
                time.sleep(10)
            else:
                self.logger.info('Success! recieved {} candles'.format(len(klines)))
                lastDate = klines[-1][0]
                klinesList.extend(klines)
                df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                self.db.store_klines(df, self.tableName)
                time.sleep(3)
        self.logger.info('Expected {} candles!'.format((endAt - startAt)/(Utility.array[self.timeFrame]*60000)))
        self.logger.info('Done! recieved {} candles'.format(len(klinesList)))
        firstDate = datetime.fromtimestamp(klinesList[0][0]/1000, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
        endDate = datetime.fromtimestamp(klinesList[-1][0]/1000, tz=timezone('utc')).strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info(f'From {firstDate} to {endDate}')

    def find_new_data(self, klines):
        try:
            df = self.db.read_klines(self.pair, self.timeFrame, 200, time.time()*1000)
        except:
            self.logger.error("Cannot read klines from db!")
        diff = klines.merge(df, how = 'outer', indicator = True).loc[ lambda x : x['_merge'] == 'left_only']
        return diff

    def main_loop(self):
        self.logger.debug("Enter main loop")
        while True:
            klines = self.get_current_klines()
            self.db.create_ohlcv_table(self.pair,self.timeFrame)
            diff = self.find_new_data(klines)
            self.db.store_klines(diff,self.tableName)
            self.logger.info (f"{diff.shape[0]} new canldes were added to {self.tableName}")
            time.sleep(Utility.array[self.timeFrame] * 60)

class Downloader():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.tablesList = self.find_tables()
        self.exchange = Exchange(self.settings).exchange
        self.logger = get_logger(__name__, settings)

    def initialize_indexes(self, table):
        downloader = DataDownloader(table[0], table[1], self.exchange, self.settings)
        downloader.main_loop()

    def find_tables(self):
        tables = []
        with open(self.settings.DATABASE_INDEXES_PATH,"r") as json_data_file:
            try:
                jsonFile = json.load(json_data_file)
            except:
                self.logger.error(f"Cannot load {self.settings.DATABASE_INDEXES_PATH}")
            ptss = jsonFile["tables"]
            for pts in ptss:
                tables.append( (pts["pair"], pts["tf"]))
        return tables

if __name__ == '__main__':
    settings = Settings(sys.argv[1])
    if os.path.exists(settings.ACCOUNT_DIR):
        downloader = Downloader(settings)
        print("Len table list:" + str(len(downloader.tablesList)))
        with concurrent.futures.ThreadPoolExecutor() as executor:        
            executor.map(downloader.initialize_indexes,downloader.tablesList)

