class Position():
    def __init__(self, id, pair, type, volume, openPrice, openAt, timeFrame, strategyName, botName, isOpen = True, leverage = 1, stopLoss = 0, takeProfit = 0, slPercent = 0, tpPercent = 0, comment="") -> None:
        self.id = id
        self.pair = pair
        self.side = type
        self.volume = volume
        self.entryPrice = openPrice
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
        self.leverage = leverage
        self.isOpen = isOpen
        self.timeFrame = timeFrame
        self.strategyName = strategyName
        self.botName = botName
        

    def calc_profit(self):
        if self.side == "buy":
            self.profit = (self.currentPrice - self.entryPrice) * self.volume - self.commission
        elif self.side == "sell":
            self.profit = (self.entryPrice - self.currentPrice) * self.volume - self.commission
        return self.profit

    def close_position(self, timestamp):
        self.closeAt = timestamp
        self.commission += self.volume * self.currentPrice * 0.0006
        self.calc_profit()
        return (self.entryPrice * self.volume) + self.profit

    def calc_equity(self):
        self.calc_profit()
        return (self.entryPrice * self.volume) + self.profit

    def to_dict(self):
        return {
            'id' : self.id,
            'pair': self.pair,
            'type': self.side,
            'volume': self.volume,
            'openPrice': self.entryPrice,
            'currentPrice': self.currentPrice,
            'openAt': self.openAt,
            'stopLoss': self.stopLoss,
            'takeProfit': self.takeProfit,
            'closeAt': self.closeAt,
            'profit': self.profit,
            'commission': self.commission,
            'comment': self.comment,
            'leverage': self.leverage,
            'isOpen': self.isOpen,
            'timeFrame': self.timeFrame,
            'strategyName': self.strategyName,
            'botName': self.botName
        }