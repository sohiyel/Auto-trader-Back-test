class PortfolioManager():
    def __init__(self, initialCapital) -> None:
        self.balance = initialCapital
        self.equity = initialCapital
        self.profit = 0.0
        self.loss = 0.0
        self.pol = 0.0
        

