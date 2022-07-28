import pytest
from src.settings import Settings
from src.userInput import UserInput
from src.tests.testValues import TestValue
from src.paramInput import ParamInput
import itertools

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "back_test"
    setting = Settings(username, task)
    return setting

def test_get_strategy_inputs_without_file(settings):
    with pytest.raises(FileNotFoundError):
        userInput = UserInput("BTC-USDT","4h","MACD","",settings=settings)
        userInput.get_strategy_inputs("MACD")

def test_get_strategy_inputs_with_optimization(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "",
                            optimization=True, settings=settings)
    expectedInputs = TestValue.inputs01
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_strategy_inputs(userInput.strategyName) == expectedReturn

def test_get_strategy_inputs_with_optimization_invalid(settings):
    userInput = UserInput("BTC-USDT", "4h", "RSIStrategy", "",
                            optimization=True, settings=settings)
    with pytest.raises(NotImplementedError):
        userInput.get_strategy_inputs(userInput.strategyName)

def test_get_strategy_inputs_without_optimization(settings):
    userInput = UserInput("BTC-USDT", "4h", "TwoEMA", "",
                            optimization=False, settings=settings)
    expectedInputs = TestValue.inputs02
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_strategy_inputs(userInput.strategyName) == expectedReturn

def test_get_bot_inputs_with_optimization(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    expectedInputs = TestValue.inputs03
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_bot_inputs() == expectedReturn

def test_get_bot_inputs_without_optimization(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=False, settings=settings)
    expectedInputs = TestValue.inputs04
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_bot_inputs() == expectedReturn

def test_find_inputs(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",randomInput=True,
                            optimization=False, settings=settings)
    userInput.find_inputs()
    expectedInputs = TestValue.inputs04
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.inputs == expectedReturn

def test_get_current_input(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    userInput.find_inputs()
    expectedInputs = TestValue.inputs03
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_current_input() == expectedReturn[0]

def test_get_strategy_names(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    expectedStrategyNames = ["OneEMA","TwoEMA"]
    assert set(userInput.get_strategy_names()) == set(expectedStrategyNames)

def test_get_input_names(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    expectedInputNames = [("len", "OneEMA", True, "cross"),
                            ("fast_len", "TwoEMA", True,"cross"),
                            ("slow_len", "TwoEMA", True,"cross"),
                            ("tp_percent", "Bot01", False,"none"),
                            ("sl_percent", "Bot01", False,"none")]
    assert set(userInput.get_input_names()) == set(expectedInputNames)

def test_calc_history_needed(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    userInput.find_inputs()
    assert userInput.calc_history_needed() == 250 * 4 * 60 * 60