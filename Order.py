class Order():
    def __init__(self, pair, type, volume, openPrice, currentPrice, openAt, stopLoss = "", target = "") -> None:
        self.pair = pair
        self.type = type
        self.volume = volume
        self.openPrice = openPrice
        self.currentPrice = currentPrice
        self.openAt = openAt
        self.stopLoss = stopLoss
        self.target = target
        self.closeAt = ""
        self.profit = 0.0
        self.commission = 0.06

    def calcProfit(self):
        if self.closeAt != "":
            self.profit = self.currentPrice - self.openPrice
        return self.profit

    def closeOrder(self, timestamp):
        self.closeAt = timestamp