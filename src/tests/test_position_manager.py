import pytest
from src.settings import Settings
from src.tests.testValues import TestValue
from src.positionManager import PositionManager
from src.utility import Utility
import time

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "download_data"
    setting = Settings(username, task)
    setting.exchange_service = ExchangeMock()
    return setting

class ExchangeMock:
    def fetch_ohlcv(self, pair, timeFrane, lastDate=""):
        klines = TestValue.klines1
        return klines
    def change_symbol_for_data(self, pair):
        return pair
    def change_symbol_for_trade(self, pair):
        return pair
    def get_contract_size(self, market, pair):
        return 0.001

class DBMock:
    def store_klines(self,df, tableName):
        print(f"A dataframe with {df.shape[0]} indexes stored in {tableName}!")
    def read_klines(self,pair, timeFrame, noCandles, lastDate):
        return TestValue.df1
    def get_ohlcv_table_name(self,pair, timeFrame):
        return pair+"_"+timeFrame
    def get_open_positions(self, pair):
        return TestValue.positionsDF01
    def get_positions(self, pair):
        positions = TestValue.positionsDF02
        return positions

def positionManager(settings):
    positionManager = PositionManager(10000, "BTC/USDT:USDT", 10, 0, "4h", "OneEMA", "", 1, settings)
    positionManager.db = DBMock()
    return positionManager

def test_init_position_manager(settings):
    positionManager = PositionManager(100000, "BTC/USDT:USDT", 10, 0, "4h", "OneEMA", "", 1, settings)

def test_check_open_position_with_valid_margin(settings):
    newMargin = 10000*settings.constantNumbers["margin_ratio"]-559.72-1
    assert positionManager(settings).check_open_position_margin(newMargin) == True

def test_check_open_position_with_invalid_margin(settings):
    newMargin = 10000*settings.constantNumbers["margin_ratio"]-559.72+1
    assert positionManager(settings).check_open_position_margin(newMargin) == False

def test_check_open_positon_with_valid_time(settings):
    dbPositions = positionManager(settings).db.get_positions("BTC/USDt:USDT")
    dbPositions["openAt"] = time.time() * 1000 - (Utility.array["4h"] * (settings.constantNumbers["open_position_delays"]+1)) * 60000
    assert positionManager(settings).check_open_position_time(dbPositions)

def test_check_open_positon_with_invalid_time(settings):
    dbPositions = positionManager(settings).db.get_positions("BTC/USDt:USDT")
    dbPositions["openAt"] = time.time() * 1000 - (Utility.array["4h"] * (settings.constantNumbers["open_position_delays"]-1)) * 60000
    assert positionManager(settings).check_open_position_time(dbPositions) == False

if __name__ == '__main__':
    print(DBMock.get_positions(DBMock,""))