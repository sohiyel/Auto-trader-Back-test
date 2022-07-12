import pytest
from src.settings import Settings
from src.singleStrategy import SingleStrategy
from src.tests.testValues import TestValue
from accounts.test.strategies.OneEMA import OneEMA

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    return setting

def test_init_single_strategy(settings):
    singleStrategy = SingleStrategy("OneEMA", TestValue.currentInput("OneEMA"),"BTC/USDT:USDT",settings,TestValue.df1)
    assert isinstance(singleStrategy.strategy, OneEMA)

def test_init_single_strategy_invalid(settings):
    with pytest.raises(FileNotFoundError):
        singleStrategy = SingleStrategy("MACD", TestValue.currentInput("OneEMA"),"BTC/USDT:USDT",settings,TestValue.df1)

def test_decider(settings):
    singleStrategy = SingleStrategy("OneEMA", TestValue.currentInput("OneEMA"),"BTC/USDT:USDT",settings,TestValue.df1)
    signal = singleStrategy.decider(TestValue.df1, 1618156800)
    assert signal == TestValue.signal01