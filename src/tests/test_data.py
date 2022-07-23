import pytest
from src.data import DataService
from src.settings import Settings
import pandas as pd
from src.tests.testValues import TestValue

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    return setting

class DBMock:
    def fetch_klines(self, pair, timeFrame, stratAt, endAt):
        return TestValue.df1
    def read_klines(self, pair, timeFrame, limit, lastState):
        return TestValue.df2

def test_init_data_service(settings):
    dataService = DataService(DBMock(), "BTC/USDT:USDT", "1m", "2021-03-09_12:00:00","2021-04-11_16:00:00", 0, settings)

def test_convert_time():
    assert DataService.convert_time("2021-03-09_12:00:00") == 1615291200

def test_fetch_klines(settings):
    dataService = DataService(DBMock(), "BTC/USDT:USDT", "1m", "2021-03-10_12:00:00","2021-04-11_16:00:00", 86400, settings)
    dataService.fetch_klines()
    assert dataService.dataFrame.iloc[-1]["timestamp"] == TestValue.df1.iloc[-1]["timestamp"]

def test_read_data_from_db(settings):
    dataService = DataService(DBMock(), "BTC/USDT:USDT", "1m", "2021-03-10_12:00:00","2021-04-11_16:00:00", 86400, settings)
    assert dataService.read_data_from_db(10,100).iloc[-1]["timestamp"] == TestValue.df2.iloc[-1]["timestamp"]

def test_read_data_from_memory(settings):
    dataService = DataService(DBMock(), "BTC/USDT:USDT", "1m", "2021-03-10_12:00:00","2021-04-11_16:00:00", 86400, settings)
    dataService.fetch_klines()
    readedDF = dataService.read_data_from_memory(10, TestValue.klines1[20][0])
    assert readedDF.iloc[0]["timestamp"] == TestValue.df1.iloc[11]["timestamp"] and readedDF.iloc[-1]["timestamp"] == TestValue.df1.iloc[20]["timestamp"]