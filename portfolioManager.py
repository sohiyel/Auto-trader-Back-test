
class PortfolioManager():
    def __init__(self, initialCapital) -> None:
        self.balance = initialCapital
        self.equity = initialCapital
        self.profit = 0.0
        self.loss = 0.0
        self.pol = 0.0
        self.numProfits = 0
        self.numLosses = 0
        
    def calcPoL(self):
        if self.loss != 0:
            self.pol = abs( self.profit / self.loss )

    def openPosition(self, volume, price, commission):
        if volume * price *  ( 1 + commission ) < self.balance:
            self.balance -= volume * price
            return True
        else:
            print ("Insufficent balance!", self.balance, price * volume)
            return False

    def closePosition(self, lastPrice, commission):
        self.balance += lastPrice

    def addProfit(self, profit):
        self.profit += profit
        self.numProfits += 1

    def addLoss(self, loss):
        self.loss += loss
        self.numLosses += 1

    def addVolume(self, volume, price, commission):
        if volume * price *  ( 1 + commission ) < self.balance:
            self.balance -= volume * price *  ( 1 + commission )
            return True
        else:
            print ("Insufficent balance!")
            return False

    def updateEquity(self, lastPrice):
        self.equity = self.balance + lastPrice
        return self.equity
