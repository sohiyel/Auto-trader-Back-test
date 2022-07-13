class Position():
    def __init__(self, id, pair, side, volume, contractSize, entryPrice, openAt, timeFrame, strategyName, botName, stopLossOrderId ='', takeProfitOrderId='', isOpen = True, leverage = 1, stopLoss = 0, takeProfit = 0, slPercent = 0, tpPercent = 0, comment="", settings="") -> None:
        self.id = id
        self.pair = pair
        self.side = side
        self.volume = volume
        self.contractSize = contractSize
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
        self.commission = settings.constantNumbers["commission"] * entryPrice * volume * self.contractSize
        self.comment = comment
        self.leverage = leverage
        self.isOpen = isOpen
        self.timeFrame = timeFrame
        self.strategyName = strategyName
        self.botName = botName
        self.stopLossOrderId = stopLossOrderId
        self.takeProfitOrderId = takeProfitOrderId
        self.settings = settings
        

    def calc_profit(self):
        if self.side == "buy":
            self.profit = ((self.currentPrice - self.entryPrice) * self.volume * self.contractSize - self.commission)
        elif self.side == "sell":
            self.profit = ((self.entryPrice - self.currentPrice) * self.volume * self.contractSize - self.commission) 
        return self.profit

    def close_position(self, timestamp):
        self.closeAt = timestamp
        self.commission += self.volume * self.currentPrice * self.settings.constantNumbers["commission"] * self.contractSize
        self.calc_profit()
        return (self.entryPrice * self.volume * self.contractSize * (1+self.settings.constantNumbers["commission"])) + self.profit

    def calc_equity(self):
        self.calc_profit()
        return (self.entryPrice * self.volume * self.contractSize) + self.profit

    def to_dict(self):
        return {
            'id' : self.id,
            'pair': self.pair,
            'side': self.side,
            'volume': self.volume,
            'contractSize': str(self.contractSize),
            'entryPrice': self.entryPrice,
            'currentPrice': str(self.currentPrice),
            'openAt': self.openAt,
            'stopLoss': str(self.stopLoss),
            'takeProfit': str(self.takeProfit),
            'closeAt': str(self.closeAt),
            'profit': str(self.profit),
            'commission': str(self.commission),
            'comment': self.comment,
            'leverage': str(self.leverage),
            'isOpen': self.isOpen,
            'timeFrame': self.timeFrame,
            'strategyName': self.strategyName,
            'botName': self.botName
        }

    def __repr__(self):
        print(self.to_dict())