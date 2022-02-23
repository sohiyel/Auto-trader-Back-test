import requests
from tfMap import tfMap

class Kucoin:
    def __init__(self, market, timeFrame):
        self.market = market
        self.timeFrame = timeFrame
        self.limit = 1440 * tfMap.array[self.timeFrame] * 60