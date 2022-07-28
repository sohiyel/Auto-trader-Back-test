import pytest
from src.simulator import Simulator
from src.settings import Settings
import pandas as pd
from src.tests.testValues import TestValue
from src.exchangePosition import ExchangePosition
import os

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "backtest"
    setting = Settings(username, task)
    setting.exchange_service = ExchangeMockSynced()
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

class DBMock:
    def fetch_klines(self, pair, timeFrame, stratAt, endAt):
        return TestValue.df1
    def read_klines(self, pair, timeFrame, limit, lastState):
        return TestValue.df2

def test_init_simulator(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 10, TestValue.currentInput("OneEMA"), True, 0, settings, DBMock())

def test_open_position(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 10, TestValue.currentInput("OneEMA"), True, 0, settings, DBMock())
    simulator.open_position(TestValue.signal03, 0.0006)
    assert len(simulator.positionManager.openPositions) == 1 and\
         simulator.positionManager.openPositions[0].pair == "BTC/USDT:USDT" and\
            simulator.positionManager.openPositions[0].entryPrice == TestValue.signal03.price

def test_close_position(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 10, TestValue.currentInput("OneEMA"), True, 0, settings, DBMock())
    simulator.open_position(TestValue.signal03, 0.0006)
    simulator.positionManager.openPositions[0].currentPrice = TestValue.signal03.price + 100
    simulator.close_position()
    assert len(simulator.positionManager.openPositions) == 0 and\
        len(simulator.positionManager.closedPositions) == 1

def test_process_order(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 0, settings, DBMock())
    simulator.process_orders(1, TestValue.signal01, 0.0006)
    assert len(simulator.positionManager.openPositions) == 1 and\
        len(simulator.positionManager.closedPositions) == 0

def test_process_order_invalid_side(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 0, settings, DBMock())
    simulator.side = "long"
    simulator.process_orders(3, TestValue.signal02, 0.0006)
    assert len(simulator.positionManager.openPositions) == 0 and\
        len(simulator.positionManager.closedPositions) == 0
    
def test_process_order_opposite_direction(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 0, settings, DBMock())
    simulator.open_position(TestValue.signal03, 0.0006)
    simulator.positionManager.openPositions[0].currentPrice = TestValue.signal03.price + 100
    simulator.process_orders(1, TestValue.signal01, 0.0006)
    assert len(simulator.positionManager.openPositions) == 1 and\
        len(simulator.positionManager.closedPositions) == 1

def test_get_data(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-10_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 72000, settings, DBMock())
    df, lastCandle = simulator.get_data(1615348800)
    assert df.iloc[-1]["timestamp"] == 1615348800000

def test_check_continue_not_hit(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 3600000, settings, DBMock())
    df, simulator.lastCandle = simulator.get_data(1615348800)
    simulator.open_position(TestValue.signal01, 0.0006)
    assert simulator.check_continue() == False

def test_check_continue_hit(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 3600000, settings, DBMock())
    df, simulator.lastCandle = simulator.get_data(1617926400)
    simulator.open_position(TestValue.signal01, 0.0006)
    assert simulator.check_continue() == True

def test_main_loop_backtest(settings):
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 3600000, settings, DBMock())
    report = simulator.main_loop()
    expectedReport = pd.read_csv(os.path.join(settings.REPORTS_DIR,"test.csv"))
    assert report.iloc[0]['Net profit percent'] == expectedReport.iloc[0]['Net profit percent']

def test_main_loop_fast_backtest(settings):
    settings.task = "fast_backtest"
    simulator = Simulator("BTC/USDT:USDT", "4h", "2021-03-09_12:00:00","2021-04-11_16:00:00",
     100000, "OneEMA", "", 1, TestValue.currentInput("OneEMA"), True, 3600000, settings, DBMock())
    report = simulator.main_loop()
    expectedReport = pd.read_csv(os.path.join(settings.REPORTS_DIR,"test.csv"))
    assert report.iloc[0]['Net profit percent'] == expectedReport.iloc[0]['Net profit percent']