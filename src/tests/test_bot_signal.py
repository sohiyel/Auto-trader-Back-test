import pytest
from src.botSignal import BotSignal
from src.settings import Settings
from src.tests.testValues import TestValue
from src.paramInput import ParamInput
from src.signalClass import SignalClass

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "back_test"
    setting = Settings(username, task)
    return setting

def botSignalWithMarketData(settings) -> BotSignal:
    botName = "Bot01"
    return BotSignal(botName, TestValue.currentInput("Bot01"), timeFrame="default",
                     pair="default", settings= settings, marketData=TestValue.df1)

def botSignalWithoutMarketData(settings) -> BotSignal:
    botName = "Bot01"
    return BotSignal(botName, TestValue.currentInput("Bot01"), timeFrame="default",
                     pair="default", settings= settings)

def test_bot_signal_strategy_names(settings):
    expectedStrategyNames = set(['TwoEMA', 'OneEMA'])
    assert set(botSignalWithMarketData(settings).strategyNames) == expectedStrategyNames

def test_get_final_decision(settings):
    signals = [
        SignalClass(longEnter=1,longExit=0,shortEnter=0,shortExit=0),
        SignalClass(longEnter=0,longExit=1,shortEnter=0,shortExit=0),
        SignalClass(longEnter=0,longExit=0,shortEnter=1,shortExit=0),
        SignalClass(longEnter=0,longExit=0,shortEnter=0,shortExit=1)
    ]
    expectedDecision = {
            "longEnter": False,
            "longExit": True,
            "shortEnter": False,
            "shortExit": True
        }
    assert botSignalWithoutMarketData(settings).get_final_decision(signals) == expectedDecision

def test_decider_with_market_data(settings):
    signal = botSignalWithMarketData(settings).decider(TestValue.df1,1617595200)
    expectedDecision = {
            "longEnter": True,
            "longExit": False,
            "shortEnter": False,
            "shortExit": True
        }
    assert signal.longEnter == expectedDecision["longEnter"] and\
            signal.longExit == expectedDecision["longExit"] and\
                signal.shortExit == expectedDecision["shortExit"] and\
                    signal.shortEnter == expectedDecision["shortEnter"]

def test_decider_without_market_data(settings):
    signal = botSignalWithoutMarketData(settings).decider(TestValue.df1)
    expectedDecision = {
            "longEnter": True,
            "longExit": False,
            "shortEnter": False,
            "shortExit": True
        }
    assert signal.longEnter == expectedDecision["longEnter"] and\
            signal.longExit == expectedDecision["longExit"] and\
                signal.shortExit == expectedDecision["shortExit"] and\
                    signal.shortEnter == expectedDecision["shortEnter"]

if __name__ == '__main__':
    print(TestValue.df1.iloc[160]['close'])