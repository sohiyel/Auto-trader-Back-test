import pytest
from src.settings import Settings
from src.tests.testValues import TestValue
from src.positionManager import PositionManager
from src.utility import Utility
import time

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
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
    def fetch_order_book(self, pair):
        return {'bids':[[2000]], 'asks':[[1999]]}
    def create_market_order(self,pair,side,volume,leverage,comment):
        return True

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
        positions = TestValue.positionsDF01
        return positions
    def add_order(self,stopLossOrderId, pair, side, amount, stopLoss, leverage, isOpen, timeFrame, strategyName, botName, positionId):
        return True
    def add_position(self,positionId, pair, side, amount, price, lastState, leverage, isOpen, timeFrame, strategyName, botName, stopLossOrderId, takeProfitOrderId):
        return True

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

def test_open_position(settings):
    pManager = positionManager(settings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert len(pManager.openPositions) == 1 and pManager.openPositions[0].pair == "BTC/USDT:USDT" and pManager.openPositions[0].entryPrice == 597.0

def test_close_position(settings):
    pManager = positionManager(settings)
    pManager.open_position(TestValue.signal03,1622216000)
    pManager.close_position(1623216000)
    assert len(pManager.openPositions) == 0 and len(pManager.closedPositions) == 1 and\
         pManager.closedPositions[0].pair == "BTC/USDT:USDT" and pManager.closedPositions[0].entryPrice == 597.0

def test_check_sl_tp(settings):
    pManager = positionManager(settings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert pManager.check_sl_tp(600,1623216000)

def test_check_sl_tp_hit_target(settings):
    pManager = positionManager(settings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert pManager.check_sl_tp(597*0.7-1,1623216000) == False

def test_check_sl_tp_hit_stop(settings):
    pManager = positionManager(settings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert pManager.check_sl_tp(597*1.1+1,1623216000) == False

def test_calc_equity(settings):
    pManager = positionManager(settings)
    pManager.open_position(TestValue.signal03,1622216000)
    pManager.openPositions[0].currentPrice = 697
    assert pManager.calc_equity() == (597 - (697 - 597)) * 10 * 0.001 - (597 * 0.001 * 10 * settings.constantNumbers["commission"])

def test_check_open_positon_with_valid_time(settings):
    dbPositions = positionManager(settings).db.get_positions("BTC/USDt:USDT")
    dbPositions["openAt"] = time.time() * 1000 - (Utility.array["4h"] * (settings.constantNumbers["open_position_delays"]+1)) * 60000
    assert positionManager(settings).check_open_position_time(dbPositions) == True

def test_check_open_positon_with_invalid_time(settings):
    dbPositions = positionManager(settings).db.get_positions("BTC/USDt:USDT")
    dbPositions["openAt"] = time.time() * 1000 - (Utility.array["4h"] * (settings.constantNumbers["open_position_delays"]-1)) * 60000
    assert positionManager(settings).check_open_position_time(dbPositions) == False




if __name__ == '__main__':
    print(DBMock.get_positions(DBMock,""))