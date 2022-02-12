class Position():
    def __init__(self, id, pair, type, volume, openPrice, openAt, stopLoss = "", takeProfit = "", comment="") -> None:
        self.id = id
        self.pair = pair
        self.type = type
        self.volume = volume
        self.openPrice = openPrice
        self.currentPrice = openPrice
        self.openAt = openAt
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.closeAt = ""
        self.profit = 0.0
        self.commission = 0.06
        self.comment = comment

    def calcProfit(self):
        if self.type == "LONG":
            self.profit = (self.currentPrice - self.openPrice) * self.volume
        elif self.type == "SHORT":
            self.profit = (self.openPrice - self.currentPrice) * self.volume
        return self.profit

    def closePosition(self, timestamp):
        self.closeAt = timestamp
        self.calcProfit()
        return self.openPrice * self.volume + self.profit