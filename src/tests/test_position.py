import pytest
from src.settings import Settings
from src.position import Position
from src.tests.testValues import TestValue

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    return setting

def test_init_position(settings):
    position = Position("flsknfj34e3f34rf","BTC/USDT:USDT","buy",1,0.001,20000,160123456,"4h","OneEMA","",slPercent=0.1,tpPercent=0.3,settings=settings)
    assert position.stopLoss == 18000 and position.takeProfit == 26000 and position.commission == settings.constantNumbers["commission"] * 20

def test_calc_buy_profit(settings):
    position = Position("flsknfj34e3f34rf","BTC/USDT:USDT","buy",10,0.001,20000,160123456,"4h","OneEMA","",slPercent=0.1,tpPercent=0.3,settings=settings)
    position.currentPrice = 25000
    position.calc_profit()
    assert position.profit == (50 - (settings.constantNumbers["commission"]*200))

def test_calc_sell_profit(settings):
    position = Position("flsknfj34e3f34rf","BTC/USDT:USDT","sell",100,0.001,20000,160123456,"4h","OneEMA","",slPercent=0.1,tpPercent=0.3,settings=settings)
    position.currentPrice = 24000
    position.calc_profit()
    assert position.profit == (-400 - (settings.constantNumbers["commission"]*2000))

def test_close_position(settings):
    position = Position("flsknfj34e3f34rf","BTC/USDT:USDT","sell",100,0.001,20000,160123456,"4h","OneEMA","",slPercent=0.1,tpPercent=0.3,settings=settings)
    position.currentPrice = 24000
    position.calc_profit()
    assert position.close_position(160123956) == (2000 * (1+settings.constantNumbers["commission"])) + (-400 - (settings.constantNumbers["commission"]*(2000+2400)))

def test_calc_equity(settings):
    position = Position("flsknfj34e3f34rf","BTC/USDT:USDT","sell",100,0.001,20000,160123456,"4h","OneEMA","",slPercent=0.1,tpPercent=0.3,settings=settings)
    position.currentPrice = 24000
    position.calc_profit()
    assert position.calc_equity() == 2000 + position.profit