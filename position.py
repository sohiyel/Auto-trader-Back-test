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
        self.commission = 0.00
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
        return (self.openPrice * self.volume) + self.profit

    def to_dict(self):
        return {
            'id' : self.id,
            'pair': self.pair,
            'type': self.type,
            'volume': self.volume,
            'openPrice': self.openPrice,
            'currentPrice': self.currentPrice,
            'openAt': self.openAt,
            'stopLoss': self.stopLoss,
            'takeProfit': self.takeProfit,
            'closeAt': self.closeAt,
            'profit': self.profit,
            'commission': self.commission,
            'comment': self.commission
        }