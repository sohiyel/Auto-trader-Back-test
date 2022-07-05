from turtle import back
from attr import s
import pytest
from src import backTestTask
from src.tests.testValues import TestValue
from src.settings import Settings
from src.backTestTask import BackTestTask

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "back_test"
    setting = Settings(username, task)
    return setting

def test_read_task_file(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.read_task_file()

def test_read_toDo(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    assert backTestTask.pair == "BTC-USDT" and backTestTask.timeFrame == "4h" and\
        backTestTask.strategyName == "OneEMA" and backTestTask.botName == "" and\
            backTestTask.startAt == "2021-01-01_00:00:00" and backTestTask.endAt == "2021-09-01_00:00:00" and\
                backTestTask.volume == 1 and backTestTask.initialCapital == 100000 and\
                    backTestTask.market == "spot" and backTestTask.optimization == False and\
                        backTestTask.randomInputs == False and backTestTask.numberOfInputs == 5

def test_task_insufficient_parameters(settings):
    backTestTask = BackTestTask(settings)
    assert backTestTask.check_task() == (False,"Insufficient task parameters")

def test_task_number_of_inputs(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    backTestTask.numberOfInputs = ""
    backTestTask.randomInputs = True
    assert backTestTask.check_task() == (False,"Number of inputs is required for random input")

def test_task_timeFrame(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    backTestTask.timeFrame = "8h"
    assert backTestTask.check_task() == (False,"Timeframe of this task is not valid")

def test_task_bot_file(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    backTestTask.botName = "Bot03"
    assert backTestTask.check_task() == (False,"Bot file does not exists")

def test_task_strategy_file(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    backTestTask.strategyName = "MacD"
    assert backTestTask.check_task() == (False,"Strategy file does not exists")

def test_task_start_and_end_date(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    backTestTask.startAt = "2022-09-01_00:00:00"
    assert backTestTask.check_task() == (False,"StartAt and EndAt are not valid")

def test_task_market_type(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    backTestTask.market = "Invalid"
    assert backTestTask.check_task() == (False,"This market type in not valid")

def test_valid_task(settings):
    backTestTask = BackTestTask(settings)
    backTestTask.jsonFile = TestValue.tasks
    backTestTask.read_toDo()
    assert backTestTask.check_task() == (True,"ok")