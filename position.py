class Position():
    def __init__(self, id, pair, type, volume, openPrice, openAt, stopLoss = 0, takeProfit = 0, slPercent = 0, tpPercent = 0, comment="") -> None:
        self.id = id
        self.pair = pair
        self.type = type
        self.volume = volume
        self.openPrice = openPrice
        self.currentPrice = openPrice
        self.openAt = openAt
        if slPercent > 0 and tpPercent > 0:
            if type == "buy":
                self.stopLoss = (1 - slPercent ) * openPrice
                self.takeProfit = (1 + tpPercent) * openPrice
            elif type == "sell":
                self.stopLoss = (1 + slPercent) * openPrice
                self.takeProfit = (1 - tpPercent) * openPrice
        elif stopLoss > 0 and takeProfit > 0:
            self.takeProfit = takeProfit
            self.stopLoss = stopLoss
        self.closeAt = ""
        self.profit = 0.0
        self.commission = 0.0006 * openPrice * volume
        self.comment = comment
        

    def calcProfit(self):
        if self.type == "buy":
            self.profit = (self.currentPrice - self.openPrice) * self.volume - self.commission
        elif self.type == "sell":
            self.profit = (self.openPrice - self.currentPrice) * self.volume - self.commission
        return self.profit

    def closePosition(self, timestamp):
        self.closeAt = timestamp
        self.commission += self.volume * self.currentPrice * 0.0006
        self.calcProfit()
        return (self.openPrice * self.volume) + self.profit

    def calcEquity(self):
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
            'comment': self.comment
        }