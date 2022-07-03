import pytest
from src.data_downloader import DataDownloader
from src.data_downloader import Downloader
from src.settings import Settings
import pandas as pd
from src.tests.testValues import TestValue

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "download_data"
    setting = Settings(username, task)
    setting.exchange_service = ExchangeMock()
    return setting

@pytest.fixture
def dataDownloader(settings) -> DataDownloader:
    pair = "BTC/USDT:USDT"
    timeFrame = "4h"
    db = DBMock()
    return DataDownloader(pair, timeFrame, settings, db)
class ExchangeMock:
    def fetch_ohlcv(self, pair, timeFrane, lastDate=""):
        klines = TestValue.klines1
        return klines
    def change_symbol_for_data(self, pair):
        return pair
class DBMock:
    def store_klines(self,df, tableName):
        print(f"A dataframe with {df.shape[0]} indexes stored in {tableName}!")
    def read_klines(self,pair, timeFrame, noCandles, lastDate):
        return TestValue.df1
    def get_ohlcv_table_name(self,pair, timeFrame):
        return pair+"_"+timeFrame

def test_get_current_klines(dataDownloader):
    dDownloader = dataDownloader
    dDownloader.get_current_klines()

def test_fetch_klines(dataDownloader):
    dataDownloader.fetch_klines(1615291200000,1618156800000)

def test_fetch_klines_invalid(dataDownloader):
    with pytest.raises(ValueError):
        dataDownloader.fetch_klines(1618156800000,1615291200000)

def test_find_new_data(dataDownloader):
    diff = dataDownloader.find_new_data(TestValue.df2)
    diff.sort_index(inplace=True)
    if diff.shape[0] == 1:
        df = pd.DataFrame([[1618171200000,59758.0,60216.0,59540.0,60092.0,1390353.0,'left_only']], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume','_merge'],index=[199])
        assert diff.iloc[0]['timestamp'] == df.iloc[0]['timestamp']

def test_find_tables(settings):
    downloader = Downloader(settings)
    testTables = [("BTC_USDT","1m"),("ETH_USDT","1m"),("SUSHI_USDT","1m")]
    assert downloader.tablesList == testTables

if __name__ == '__main__':
    diff = TestValue.df2.merge(TestValue.df1, how = 'outer', indicator = True).loc[ lambda x : x['_merge'] == 'left_only']
    print(diff.iloc[0]['high'])