class Position():
    def __init__(self, id, pair, type, volume, openPrice, currentPrice, openAt, stopLoss = "", takeProfit = "", comment="") -> None:
        self.id = id
        self.pair = pair
        self.type = type
        self.volume = volume
        self.openPrice = openPrice
        self.currentPrice = currentPrice
        self.openAt = openAt
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.closeAt = ""
        self.profit = 0.0
        self.commission = 0.06
        self.comment = comment

    def calcProfit(self):
        if self.closeAt != "":
            self.profit = self.currentPrice - self.openPrice
        return self.profit

    def closePosition(self, timestamp):
        self.closeAt = timestamp