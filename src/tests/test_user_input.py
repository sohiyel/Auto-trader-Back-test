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
    expectedInputs = [[ParamInput("len",150,"OneEMA",True,150,250,100,True),
                        ParamInput("len",250,"OneEMA",True,150,250,100,True)],
                        [ParamInput("sl_percent",0.1,"OneEMA",False,0.1,0.4,0.1,False)],
                        [ParamInput("tp_percent",0.3,"OneEMA",False,0.3,0.51,0.1,False)]]
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
    expectedInputs = [[ParamInput("fast_len",20,"TwoEMA",True)],
                        [ParamInput("slow_len",100,"TwoEMA",True)],
                        [ParamInput("sl_percent",0.1,"TwoEMA",False)],
                        [ParamInput("tp_percent",0.3,"TwoEMA",False)]]
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_strategy_inputs(userInput.strategyName) == expectedReturn

def test_get_bot_inputs_with_optimization(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    expectedInputs = [[ParamInput("len",150,"OneEMA",True,150,251,100,True),
                        ParamInput("len",250,"OneEMA",True,150,251,100,True)],
                        [ParamInput("fast_len",20,"TwoEMA",True,20,31,10,True),
                        ParamInput("fast_len",30,"TwoEMA",True,20,31,10,True)],
                        [ParamInput("slow_len",100,"TwoEMA",True,50,101,50,False)],
                        [ParamInput("sl_percent",0.1,"Bot01",False,0.1,0.4,0.1,False)],
                        [ParamInput("tp_percent",0.3,"Bot01",False,0.3,0.51,0.1,False)]]
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_bot_inputs() == expectedReturn

def test_get_bot_inputs_without_optimization(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=False, settings=settings)
    expectedInputs = [[ParamInput("len",250,"OneEMA",True)],
                        [ParamInput("fast_len",20,"TwoEMA",True)],
                        [ParamInput("slow_len",100,"TwoEMA",True)],
                        [ParamInput("sl_percent",0.1,"Bot01",False)],
                        [ParamInput("tp_percent",0.3,"Bot01",False)]]
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.get_bot_inputs() == expectedReturn

def test_find_inputs(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",randomInput=True,
                            optimization=False, settings=settings)
    userInput.find_inputs()
    expectedInputs = [[ParamInput("len",250,"OneEMA",True)],
                        [ParamInput("fast_len",20,"TwoEMA",True)],
                        [ParamInput("slow_len",100,"TwoEMA",True)],
                        [ParamInput("sl_percent",0.1,"Bot01",False)],
                        [ParamInput("tp_percent",0.3,"Bot01",False)]]
    expectedReturn = list( itertools.product( *expectedInputs ) )
    assert userInput.inputs == expectedReturn

def test_get_current_input(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    userInput.find_inputs()
    expectedInputs = [[ParamInput("len",150,"OneEMA",True,150,251,100,True),
                        ParamInput("len",250,"OneEMA",True,150,251,100,True)],
                        [ParamInput("fast_len",20,"TwoEMA",True,20,31,10,True),
                        ParamInput("fast_len",30,"TwoEMA",True,20,31,10,True)],
                        [ParamInput("slow_len",100,"TwoEMA",True,50,101,50,False)],
                        [ParamInput("sl_percent",0.1,"Bot01",False,0.1,0.4,0.1,False)],
                        [ParamInput("tp_percent",0.3,"Bot01",False,0.3,0.51,0.1,False)]]
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
    expectedInputNames = [("len", "OneEMA", True),
                            ("fast_len", "TwoEMA", True),
                            ("slow_len", "TwoEMA", True),
                            ("tp_percent", "Bot01", False),
                            ("sl_percent", "Bot01", False)]
    assert set(userInput.get_input_names()) == set(expectedInputNames)

def test_calc_history_needed(settings):
    userInput = UserInput("BTC-USDT", "4h", "OneEMA", "Bot01",
                            optimization=True, settings=settings)
    userInput.find_inputs()
    assert userInput.calc_history_needed() == 250 * 4 * 60 * 60