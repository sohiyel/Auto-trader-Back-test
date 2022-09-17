import pytest
from src.settings import Settings
from src.tests.testValues import TestValue
from src.positionManager import PositionManager
from src.utility import Utility
from src.exchangePosition import ExchangePosition
import time

@pytest.fixture
def syncedSettings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    setting.exchange_service = ExchangeMockSynced()
    return setting

@pytest.fixture
def notSyncedSettings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    setting.exchange_service = ExchangeMockNotSynced()
    return setting

class ExchangeMockSynced:
    def fetch_ohlcv(self, pair, timeFrane, lastDate=""):
        klines = TestValue.klines1
        return klines
    def change_symbol_for_data(self, pair):
        return pair
    def change_symbol_for_trade(self, pair):
        return "BTC/USDT:USDT"
    def get_contract_size(self, market, pair):
        return 0.001
    def fetch_order_book(self, pair):
        return {'bids':[[2000]], 'asks':[[1999]]}
    def create_market_order(self,pair,side,volume,leverage=1,comment=""):
        if volume == 10000.0:
            return True
        raise ValueError
    def fetch_positions(self):
        ep = ExchangePosition("BTC/USDT:USDT","sell",10000,0.001,1)
        return [ep]
    def fetch_balance(self, pair):
        return {'Balance': 10, 'Equity': 10}

class ExchangeMockNotSynced:
    def fetch_ohlcv(self, pair, timeFrane, lastDate=""):
        klines = TestValue.klines1
        return klines
    def change_symbol_for_data(self, pair):
        return pair
    def change_symbol_for_trade(self, pair):
        return "BTC/USDT:USDT"
    def get_contract_size(self, market, pair):
        return 0.001
    def fetch_order_book(self, pair):
        return {'bids':[[2000]], 'asks':[[1999]]}
    def create_market_order(self,pair,side,volume,leverage=1,comment=""):
        return True
    def fetch_positions(self):
        ep = ExchangePosition("BTC/USDT:USDT","sell",100,0.001,1)
        return [ep]
    def close_positions(self,pair=""):
        return True
    def fetch_balance(self, pair):
        return {'Balance': 20, 'Equity': 20}

class DBMockSynced:
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
    def add_order(self,stopLossOrderId, pair, side, amount, stopLoss, leverage, isOpen, timeFrame, strategyName, botName, positionId):
        return True
    def add_position(self,positionId, pair, side, amount, price, lastState, leverage, isOpen, timeFrame, strategyName, botName, stopLossOrderId, takeProfitOrderId):
        return True
    def close_position(self, id):
        return True
    def close_order_by_positionId(self, id):
        return True

def positionManagerSynced(syncedSettings):
    positionManager = PositionManager(10000, "BTC/USDT:USDT", 10, 0, 0, "4h", "OneEMA", "", 1, syncedSettings)
    positionManager.db = DBMockSynced()
    return positionManager

def test_init_position_manager(syncedSettings):
    positionManager = PositionManager(100000, "BTC/USDT:USDT", 10, 0, 0, "4h", "OneEMA", "", 1, syncedSettings)

def test_check_open_position_with_valid_margin(syncedSettings):
    newMargin = 10000*syncedSettings.constantNumbers["max_of_each_pair_margins"]-559.72-1
    assert positionManagerSynced(syncedSettings).check_open_available_balance(newMargin) == True

def test_check_open_position_with_invalid_margin(syncedSettings):
    newMargin = 10000*syncedSettings.constantNumbers["max_of_each_pair_margins"]-559.72+1
    assert positionManagerSynced(syncedSettings).check_open_available_balance(newMargin) == False

def test_open_position(syncedSettings):
    pManager = positionManagerSynced(syncedSettings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert len(pManager.openPositions) == 1 and\
         pManager.openPositions[0].pair == "BTC/USDT:USDT" and\
             pManager.openPositions[0].entryPrice == 597.0 and\
                 pManager.openPositions[0].volume == 10

def test_close_position(syncedSettings):
    pManager = positionManagerSynced(syncedSettings)
    pManager.open_position(TestValue.signal03,1622216000)
    pManager.close_position(1623216000)
    assert len(pManager.openPositions) == 0 and len(pManager.closedPositions) == 1 and\
         pManager.closedPositions[0].pair == "BTC/USDT:USDT" and pManager.closedPositions[0].entryPrice == 597.0

def test_check_sl_tp(syncedSettings):
    pManager = positionManagerSynced(syncedSettings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert pManager.check_sl_tp(600,1623216000)

def test_check_sl_tp_hit_target(syncedSettings):
    pManager = positionManagerSynced(syncedSettings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert pManager.check_sl_tp(597*0.7-1,1623216000) == False

def test_check_sl_tp_hit_stop(syncedSettings):
    pManager = positionManagerSynced(syncedSettings)
    pManager.open_position(TestValue.signal03,1622216000)
    assert pManager.check_sl_tp(597*1.1+1,1623216000) == False

def test_calc_equity(syncedSettings):
    pManager = positionManagerSynced(syncedSettings)
    pManager.open_position(TestValue.signal03,1622216000)
    pManager.openPositions[0].currentPrice = 697
    assert pManager.calc_equity() == (597 - (697 - 597)) * 10 * 0.001 - (597 * 0.001 * 10 * syncedSettings.constantNumbers["commission"])

def test_sync_position_future_synced(syncedSettings):
    pManager = positionManagerSynced(syncedSettings)
    syncResult = pManager.sync_positions()
    assert syncResult == True and len(pManager.openPositions) == 1

def test_sync_position_future_not_synced(notSyncedSettings):
    pManager = positionManagerSynced(notSyncedSettings)
    syncResult = pManager.sync_positions()
    assert syncResult == True and len(pManager.openPositions) == 0

def test_sync_position_spot_synced(syncedSettings):
    syncedSettings.isSpot = True
    pManager = positionManagerSynced(syncedSettings)
    syncResult = pManager.sync_positions()
    assert syncResult == True and len(pManager.openPositions) == 1

def test_sync_position_spot_not_synced(notSyncedSettings):
    notSyncedSettings.isSpot = True
    pManager = positionManagerSynced(notSyncedSettings)
    syncResult = pManager.sync_positions()
    assert syncResult == True and len(pManager.openPositions) == 0

def test_check_open_positon_with_valid_time(syncedSettings):
    dbPositions = positionManagerSynced(syncedSettings).db.get_positions("BTC/USDt:USDT")
    dbPositions["openAt"] = time.time() * 1000 - (Utility.array["4h"] * (syncedSettings.constantNumbers["open_position_delays"]+1)) * 60000
    assert positionManagerSynced(syncedSettings).check_open_position_time(dbPositions) == True

def test_check_open_positon_with_invalid_time(syncedSettings):
    dbPositions = positionManagerSynced(syncedSettings).db.get_positions("BTC/USDt:USDT")
    dbPositions["openAt"] = time.time() * 1000 - (Utility.array["4h"] * (syncedSettings.constantNumbers["open_position_delays"]-1)) * 60000
    assert positionManagerSynced(syncedSettings).check_open_position_time(dbPositions) == False