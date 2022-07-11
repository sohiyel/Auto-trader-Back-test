import pytest
from src.settings import Settings
from src.portfolioManager import PortfolioManager
from src.tests.testValues import TestValue
from src.position import Position

@pytest.fixture
def settings() -> Settings:
    username = "test"
    task =  "trade"
    setting = Settings(username, task)
    setting.exchange_service = ExchangeMock()
    return setting

class ExchangeMock:
    def get_contract_size(self, markets, pair):
        return 0.001
    def fetch_balance(self):
        return {'Equity': 2123, 'Balance':100000}
    def change_symbol_for_data(self, pair):
        return pair

def test_init_portfolio_manager(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    assert portfolioManager.equity == 2123 and portfolioManager.initialCapital == 100000 and portfolioManager.contractSize == 0.001

def test_calc_pol(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    portfolioManager.profit = 1000
    portfolioManager.loss = 25
    assert portfolioManager.calc_poL() == 40

def test_calc_pol_with_ziro_division(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    portfolioManager.profit = 1000
    portfolioManager.loss = 0
    assert portfolioManager.calc_poL() == "infinite"

def test_open_position(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    volume = 10
    price = 25
    commission = 0.0006
    portfolioManager.open_position(volume, price, commission)
    assert portfolioManager.balance == 100000 - (volume * price * portfolioManager.contractSize * (1 + commission))

def test_open_position_invalid(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    volume = 1000
    price = 2500
    commission = 0.0006
    assert portfolioManager.open_position(volume, price, commission) == False

def test_close_position(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    volume = 10
    price = 25
    commission = 0.0006
    portfolioManager.open_position(volume, price, commission)
    portfolioManager.close_position(212)
    assert portfolioManager.balance == 100000 - (volume * price * portfolioManager.contractSize * (1 + commission)) + 212

def test_add_profit(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    portfolioManager.add_profit(123)
    assert portfolioManager.profit == 123 and portfolioManager.numProfits == 1

def test_add_profit_invalid(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    with pytest.raises(ValueError):
        portfolioManager.add_profit(-123)

def test_add_loss(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    portfolioManager.add_loss(-134)
    assert portfolioManager.loss == -134 and portfolioManager.numLosses == 1

def test_add_loss_invalid(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    with pytest.raises(ValueError):
        portfolioManager.add_loss(134)

def test_add_volume(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    volume = 10
    price = 25
    commission = 0.0006
    portfolioManager.open_position(volume, price, commission)
    portfolioManager.add_volume(volume, price, commission)
    assert round(portfolioManager.balance,4) == 100000 - (volume * price * portfolioManager.contractSize * (1 + commission)) * 2

def test_update_equity(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    portfolioManager.update_equity(123)
    assert portfolioManager.equity == 100123

def test_get_equity(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    portfolioManager.get_equity()
    assert portfolioManager.equity == 2123 and portfolioManager.balance == 100000

def test_report(settings):
    portfolioManager = PortfolioManager("BTC/USDT:USDT", "4h", "OneEMA", 1000, settings)
    portfolioManager.equities=[99983.0986,99975.2118,99963.0124,99973.79921,99979.40889]
    portfolioManager.balance=99979.40889
    report = portfolioManager.report(TestValue.positions)
    expectedReport = {
            "netProfit" : round(-20.59111,4),
            "netProfitPercent" : round(-0.02059111,4),
            "netProfitPercentLongs" : round(0.002899998,4),
            "netProfitPercentShorts" : round(-0.02349111,4),
            "percentProfitable" : round(66.66666667,4),
            "percentProfitableLongs" : 100,
            "percentProfitableShorts" : 50,
            "profitFactor" : round(0.4432968586,4),
            "profitFactorLongs" : round(1.367702371,4),
            "profitFactorShorts" : round(0.1927672754,4),
            "totalClosedTrades": 5,
            "totalLongTrades" : 2,
            "totalShortTrades" : 3,
            "maxDrawDown": round(36.987598,4),
            "maxDrawDownPercent" : round(0.036987598,4),
        }
    assert report == expectedReport

if __name__ == '__main__':
    for p in TestValue.positions:
        try:
            print(p)
        except Exception as e:
            print(str(e))
            continue