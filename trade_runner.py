from data import DataService
from trader import Trader

# spotData = DataService('spot', "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00")
#futuresData = DataService('futures', ".KXBT", 240, "2021-01-01", "2022-01-01")

trader = Trader(market = "spot",
                pair = "BTC-USDT",
                timeFrame = "4hour",
                startAt = "2021-01-01 00:00:00",
                endAt = "2021-09-01 00:00:00",
                initialCapital = 100000,
                strategyName = "RSIStrategy",
                botName= "Bot02",
                volume = 1)
# trader = Trader("spot", "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00", 100000, [])