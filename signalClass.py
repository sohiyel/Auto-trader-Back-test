class SignalClass():
    def __init__(self, pair="", type="", volume=1, price=0, stopLoss=0, takeProfit=0, slPercent=0, tpPercent=0, comment="", longEnter = 0, longExit = 0, shortEnter = 0, shortExit = 0) -> None:
        self.pair = pair
        self.type = type
        self.volume = volume
        self.price = price
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.slPercent = slPercent
        self.tpPercent =  tpPercent
        self.comment = comment
        self.longEnter = longEnter
        self.longExit = longExit
        self.shortEnter = shortEnter
        self.shortExit = shortExit