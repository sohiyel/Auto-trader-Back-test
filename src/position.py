from account.settings.settings import Settings

class Position():
    def __init__(self, id, pair, side, volume, entryPrice, openAt, timeFrame, strategyName, botName, isOpen = True, leverage = 1, stopLoss = 0, takeProfit = 0, slPercent = 0, tpPercent = 0, comment="") -> None:
        self.id = id
        self.pair = pair
        self.side = side
        self.volume = volume
        self.entryPrice = entryPrice
        self.currentPrice = entryPrice
        self.openAt = openAt
        self.takeProfit = 0
        self.stopLoss = 0
        if slPercent > 0 and tpPercent > 0:
            if side == "buy":
                self.stopLoss = (1 - slPercent ) * entryPrice
                self.takeProfit = (1 + tpPercent) * entryPrice
            elif side == "sell":
                self.stopLoss = (1 + slPercent) * entryPrice
                self.takeProfit = (1 - tpPercent) * entryPrice
        elif stopLoss > 0 and takeProfit > 0:
            self.takeProfit = takeProfit
            self.stopLoss = stopLoss
        self.closeAt = ""
        self.profit = 0.0
        self.commission = Settings.constantNumbers["commission"] * entryPrice * volume
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
        self.commission += self.volume * self.currentPrice * Settings.constantNumbers["commission"]
        self.calc_profit()
        return (self.entryPrice * self.volume) + self.profit

    def calc_equity(self):
        self.calc_profit()
        return (self.entryPrice * self.volume) + self.profit

    def to_dict(self):
        return {
            'id' : self.id,
            'pair': self.pair,
            'side': self.side,
            'volume': self.volume,
            'entryPrice': self.entryPrice,
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