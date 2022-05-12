import sys
from src.back_test_runner import BackTestRunner
from src.trade_runner import TradeRunner
from src.data_downloader import DataDownloader, Downloader
import concurrent.futures
import time
from src.settings import Settings
import os
from threading import Thread
from src.data import DataService
from src.tfMap import tfMap

def run_back_test(fast):
    tradeRunner = BackTestRunner(settings, fast)
    while True:
        tradeRunner.start_task()
        time.sleep(5)

def run_trade():
    tradeRunner = TradeRunner(settings)
    tradeRunner.initialize_indexes(tradeRunner.tradeIndexList[0])
    # with concurrent.futures.ThreadPoolExecutor() as executor:        
    #     executor.map(tradeRunner.initialize_indexes,tradeRunner.tradeIndexList)

def run_data_downloader():
    downloader = Downloader(settings)
    with concurrent.futures.ThreadPoolExecutor() as executor:        
        executor.map(downloader.initialize_indexes,downloader.tablesList)

def download_data(pair, timeframe, startAt, endAt):
    downloader = DataDownloader(pair, timeframe, settings)
    startAtTs = DataService.convert_time(startAt) * 1000
    endAtTs = DataService.convert_time(endAt) * 1000
    print(startAtTs, endAtTs)
    downloader.fetch_klines(startAtTs, endAtTs)

if __name__ == '__main__':
    if sys.argv[1] == "backtest":
        settings = Settings(sys.argv[2])
        if os.path.exists(settings.ACCOUNT_DIR):
            run_back_test(False)
        else:
            print (f"There is no account with this informations!")
    if sys.argv[1] == "fast_backtest":
        settings = Settings(sys.argv[2])
        if os.path.exists(settings.ACCOUNT_DIR):
            run_back_test(True)
        else:
            print (f"There is no account with this informations!")
    elif sys.argv[1] == "trade":
        settings = Settings(sys.argv[2])
        if os.path.exists(settings.ACCOUNT_DIR):
            thread01 = Thread(target= run_data_downloader)
            thread01.start()
            time.sleep(5)
            thread02 = Thread(target=run_trade)
            thread02.start()
        else:
            print (f"There is no account with this informations!")
    elif sys.argv[1] == "live_data":
        settings = Settings(sys.argv[2])
        if os.path.exists(settings.ACCOUNT_DIR):
            run_data_downloader()
        else:
            print (f"There is no account with this informations!")
    elif sys.argv[1] == "download_data":
        settings = Settings(sys.argv[2])
        if os.path.exists(settings.ACCOUNT_DIR):
            download_data(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
        else:
            print (f"There is no account with this informations!")
    else:
        print ("Wrong command!")