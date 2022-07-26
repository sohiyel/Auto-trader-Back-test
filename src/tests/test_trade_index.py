import pytest
from src.tradeIndex import TradeIndex
from src.settings import Settings
from src.userInput import UserInput

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    return setting

def test_init_trade_index(settings):
    tradeIndex = TradeIndex(settings)
    expectedIndexes = [UserInput("SUSHI-USDT","1m","Test01","","both",1,1,0,settings=settings)]
    assert tradeIndex.indexes == expectedIndexes