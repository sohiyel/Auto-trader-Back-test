from numpy import isin
import pytest
from src.settings import Settings
from src.signalManager import SignalManager
from src.tests.testValues import TestValue
from src.singleStrategy import SingleStrategy
from src.botSignal import BotSignal
from src.signalClass import SignalClass

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    return setting

def test_init_signal_manager_without_bot(settings):
    signalManager = SignalManager("OneEMA", "", TestValue.currentInput("OneEMA"), "BTC/USDT:USDT", settings,"")
    assert isinstance(signalManager.signal, SingleStrategy)

def test_init_signal_manager_with_bot(settings):
    signalManager = SignalManager("OneEMA", "Bot01", TestValue.currentInput("OneEMA"), "BTC/USDT:USDT", settings,"")
    assert isinstance(signalManager.signal, BotSignal)

def test_get_signal(settings):
    signalManager = SignalManager("OneEMA", "", TestValue.currentInput("OneEMA"), "BTC/USDT:USDT", settings,"")
    assert isinstance(signalManager.getSignal(TestValue.df1),SignalClass)