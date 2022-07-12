import pytest
from src.settings import Settings
from src.orderManager import OrderManager
from src.tests.testValues import TestValue
from src.signalManager import SignalManager

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    return setting

class SignalManagerBuyMock:
    def getSignal(self,marketData, timeStamp):
        return TestValue.signal01

class SignalManagerSellMock:
    def getSignal(self,marketData, timeStamp):
        return TestValue.signal02

def test_init_order_manager(settings):
    orderManager = OrderManager(1000, "OneEMA", "4h", "Bot01", TestValue.currentInput("Bot01"), "BTC/USDT:USDT", settings, TestValue.df1)
    assert isinstance(orderManager.signalManager,SignalManager)

def test_decider_buy(settings):
    orderManager = OrderManager(1000, "OneEMA", "4h", "Bot01", TestValue.currentInput("Bot01"), "BTC/USDT:USDT", settings, TestValue.df1)
    orderManager.signalManager = SignalManagerBuyMock()
    assert orderManager.decider(TestValue.df1,1000,1000,10,10,1618156800) == [1,TestValue.signal01]

def test_decider_with_same_signal_buy(settings):
    orderManager = OrderManager(1000, "OneEMA", "4h", "Bot01", TestValue.currentInput("Bot01"), "BTC/USDT:USDT", settings, TestValue.df1)
    orderManager.signalManager = SignalManagerBuyMock()
    orderManager.lastSignal = 1
    assert orderManager.decider(TestValue.df1,1000,1000,10,10,1618156800) == [0,TestValue.signal01]

def test_decider_with_opposite_signal_buy(settings):
    orderManager = OrderManager(1000, "OneEMA", "4h", "Bot01", TestValue.currentInput("Bot01"), "BTC/USDT:USDT", settings, TestValue.df1)
    orderManager.signalManager = SignalManagerBuyMock()
    orderManager.lastSignal = 3
    assert orderManager.decider(TestValue.df1,1000,1000,10,10,1618156800) == [1,TestValue.signal01]

def test_decider_sell(settings):
    orderManager = OrderManager(1000, "OneEMA", "4h", "Bot01", TestValue.currentInput("Bot01"), "BTC/USDT:USDT", settings, TestValue.df1)
    orderManager.signalManager = SignalManagerSellMock()
    assert orderManager.decider(TestValue.df1,1000,1000,10,10,1618156800) == [3,TestValue.signal02]

def test_decider_with_same_signal_sell(settings):
    orderManager = OrderManager(1000, "OneEMA", "4h", "Bot01", TestValue.currentInput("Bot01"), "BTC/USDT:USDT", settings, TestValue.df1)
    orderManager.signalManager = SignalManagerSellMock()
    orderManager.lastSignal = 3
    assert orderManager.decider(TestValue.df1,1000,1000,10,10,1618156800) == [0,TestValue.signal02]

def test_decider_with_opposite_signal_sell(settings):
    orderManager = OrderManager(1000, "OneEMA", "4h", "Bot01", TestValue.currentInput("Bot01"), "BTC/USDT:USDT", settings, TestValue.df1)
    orderManager.signalManager = SignalManagerSellMock()
    orderManager.lastSignal = 1
    assert orderManager.decider(TestValue.df1,1000,1000,10,10,1618156800) == [3,TestValue.signal02]