class SignalManager():
    def __init__(self, market, initialCapital) -> None:
        self.market = market
        self.initialCapital = initialCapital
        self.equity = initialCapital
        self.positionSize = 0
        self.positionAveragePrice = 0