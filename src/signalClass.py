class SignalClass():
    def __init__(self, pair="", side="", volume=1, price=0, stopLoss=0, takeProfit=0, slPercent=0, tpPercent=0, comment="", longEnter = 0, longExit = 0, shortEnter = 0, shortExit = 0) -> None:
        self.pair = pair
        self.side = side
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

    def __eq__(self, other):
        if not isinstance(other, SignalClass):
            return NotImplemented
        return self.pair == other.pair and self.price == other.price and self.slPercent == other.slPercent and\
            self.tpPercent == other.tpPercent and self.comment == other.comment and self.longExit == other.longExit and\
                self.longExit == other.longExit and self.shortEnter == other.shortEnter and self.shortExit == other.shortExit

    def __repr__(self):
        print(self.to_dict())
    
    def to_dict(self):
        return {
            'pair' : self.pair,
            'volume': self.volume,
            'price': self.price,
            'longEnter': self.longEnter,
            'longExit' : self.longExit,
            'shortEnter' : self.shortEnter,
            'shortExit': self.shortExit
        }                