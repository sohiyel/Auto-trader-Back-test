from data import DataService
from trader import Trader

# spotData = DataService('spot', "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00")
#futuresData = DataService('futures', ".KXBT", 240, "2021-01-01", "2022-01-01")

trader = Trader("spot", "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-02 00:00:00", 100000, "PriceAction",1)
# trader = Trader("spot", "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00", 100000, [])