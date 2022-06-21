import sys
from src.exchanges.exchange import Exchange
from src.back_test_runner import BackTestRunner
from src.trade_runner import TradeRunner
from src.data_downloader import DataDownloader, Downloader
import concurrent.futures
import time
from src.settings import Settings
import os
from threading import Thread
from src.data import DataService
from src.utility import Utility
from src.logManager import LogService
from src.markets import Markets
from src.databaseManager import DatabaseManager
from src.terminator import Terminator

settings = Settings(sys.argv[2], sys.argv[1])

logService = LogService(__name__, settings)
logger = logService.logger  #get_logger(__name__, settings)

def run_back_test():
    tradeRunner = BackTestRunner(settings)
    while True:
        tradeRunner.start_task()
        time.sleep(5)

def run_trade():
    tradeRunner = TradeRunner(settings)
    # tradeRunner.initialize_indexes(tradeRunner.tradeIndexList[0])
    with concurrent.futures.ThreadPoolExecutor() as executor:        
        executor.map(tradeRunner.initialize_indexes,tradeRunner.tradeIndexList)

def run_data_downloader():
    downloader = Downloader(settings)
    # downloader.initialize_indexes(downloader.tablesList[0])
    with concurrent.futures.ThreadPoolExecutor() as executor:        
        executor.map(downloader.initialize_indexes,downloader.tablesList)

def download_data(pair, timeframe, startAt, endAt):
    downloader = DataDownloader(pair, Utility.unify_timeframe(timeframe, settings.exchange), settings)
    startAtTs = DataService.convert_time(startAt) * 1000
    endAtTs = DataService.convert_time(endAt) * 1000
    downloader.db.create_ohlcv_table(pair, timeframe)
    downloader.fetch_klines(startAtTs, endAtTs)

def get_market_data():
    market = Markets(settings)
    market.load_market()
    market.write_to_file()

def set_up_tables():
    dbManager = DatabaseManager(settings, "Nan", "Nan")
    dbManager.set_up_tables()
    dbManager.conn.close()

def store_csv_to_db(deleteFile=False):
    dbManager = DatabaseManager(settings, "Nan", "Nan")
    dbManager.store_csv_to_db(deleteFile)
    dbManager.conn.close()

def terminate():
    terminator = Terminator(settings)
    terminator.close_all_positions()


if __name__ == '__main__':
    settings = Settings(sys.argv[2], sys.argv[1])
    settings.exchange_service = Exchange(settings).exchange
    if os.path.exists(settings.ACCOUNT_DIR):
        if sys.argv[1] == "backtest":
            logger.info ("Start backtesting!")
            run_back_test()
        elif sys.argv[1] == "fast_backtest":
            logger.info ("Start fast backtesting!")
            run_back_test()
        elif sys.argv[1] == "trade":
            logger.info ("Start trading!")
            get_market_data()
            set_up_tables()
            thread01 = Thread(target= run_data_downloader)
            thread01.start()
            time.sleep(5)
            thread02 = Thread(target=run_trade)
            thread02.start()
        elif sys.argv[1] == "live_data":
            logger.info ("Start downloading live data!")
            run_data_downloader()
        elif sys.argv[1] == "download_data":
            logger.info ("Start downloading backtest data!")
            download_data(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
        elif sys.argv[1] == "load_markets":
            logger.info ("Start downloading market data!")
            get_market_data()
        elif sys.argv[1] == "setup_tables":
            logger.info ("Start setuping tables!")
            set_up_tables()
        elif sys.argv[1] == "csv_to_db":
            logger.info ("Start storing data!")
            if len(sys.argv) > 3:
                store_csv_to_db(True)
            else:
                store_csv_to_db()
        elif sys.argv[1] == "terminate":
            logger.info ("Terminating all positions!")
            get_market_data()
            terminate()
        else:
            logger.error ("Wrong command!")