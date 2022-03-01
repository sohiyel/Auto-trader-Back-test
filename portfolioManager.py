
class PortfolioManager():
    def __init__(self, initialCapital) -> None:
        self.initialCapital = initialCapital
        self.balance = initialCapital
        self.equity = initialCapital
        self.profit = 0.0
        self.loss = 0.0
        self.pol = 0.0
        self.numProfits = 0
        self.numLosses = 0
        self.balances = []
        self.equities = []
        
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

    def report(self, closedPositions):
        numOfTrades = len(closedPositions)
        numOfLongs = 0
        numOfShorts = 0
        sumOfLongs = 0
        sumOfShorts = 0
        numOfWinLongs = 0
        numOfWinShorts = 0
        sumOfWinLongs = 0
        sumOfWinShorts = 0
        sumOfLossLongs = 0
        sumOfLossShorts = 0
        for p in closedPositions:
            if p.type == "LONG":
                sumOfLongs += p.profit
                numOfLongs += 1
                if p.profit > 0:
                    numOfWinLongs += 1
                    sumOfWinLongs += p.profit
                else:
                    sumOfLossLongs += p.profit
            else:
                sumOfShorts += p.profit
                numOfShorts += 1
                if p.profit > 0:
                    numOfWinShorts += 1
                    sumOfWinShorts += p.profit
                else:
                    sumOfLossShorts += p.profit
        return {
            "netProfit" : self.balance - self.initialCapital,
            "netProfitPercent" : self.balance - self.initialCapital / self.initialCapital * 100,
            "netProfitPercentLongs" : sumOfLongs / self.initialCapital * 100,
            "netProfitPercentShorts" : sumOfShorts / self.initialCapital * 100,
            "percentProfitable" : self.numProfits / numOfTrades * 100,
            "percentProfitableLongs" : numOfWinLongs / numOfTrades * 100,
            "percentProfitableShorts" : numOfWinShorts / numOfTrades * 100,
            "profitFactor" : self.profit / self.loss * -1,
            "profitFactorLongs" : sumOfWinLongs / sumOfLossLongs * -1,
            "profitFactorShorts" : sumOfWinShorts / sumOfLossShorts * -1,
            "totalClosedTrades": numOfTrades,
            "totalLongTrades" : numOfLongs,
            "totalShortTrades" : numOfShorts,
            "maxDrawDown": (self.initialCapital - min(self.equities)) / self.initialCapital,
            "maxDrawDownPercent" : (self.initialCapital - min(self.equities)) / self.initialCapital * 100,
        }
