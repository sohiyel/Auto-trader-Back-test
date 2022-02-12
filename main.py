from data import DataService
from trader import Trader

spotData = DataService('spot', "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00")
#futuresData = DataService('futures', ".KXBT", 240, "2021-01-01", "2022-01-01")

trader = Trader("BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00", 10000, [])
# print(spotData.dataFrame.loc[spotData.dataFrame['timestamp'] == "2021-01-03 00:00:00"])