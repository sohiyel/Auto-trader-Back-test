from src.markets import Markets

class PortfolioManager():
    def __init__(self, pair, initialCapital=1, settings="", exchange="") -> None:
        self.settings = settings
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
        self.exchange = exchange
        self.contractSize = Markets(self.settings).get_contract_size(pair)
        
    def calc_poL(self):
        if self.loss != 0:
            self.pol = abs( self.profit / self.loss )

    def open_position(self, volume, price, commission):
        if volume * float(price) *  ( 1 + commission ) * self.contractSize < self.balance:
            self.balance -= volume * price * self.contractSize
            return True
        else:
            print ("Insufficent balance!", self.balance, price * volume * self.contractSize)
            return False

    def close_position(self, lastPrice, commission):
        self.balance += lastPrice

    def add_profit(self, profit):
        self.profit += profit
        self.numProfits += 1

    def add_loss(self, loss):
        self.loss += loss
        self.numLosses += 1

    def add_volume(self, volume, price, commission):
        if volume * price *  ( 1 + commission ) * self.contractSize < self.balance:
            self.balance -= volume * price *  ( 1 + commission ) * self.contractSize
            return True
        else:
            print ("Insufficent balance!")
            return False

    def update_equity(self, lastPrice):
        self.equity = self.balance + lastPrice
        return self.equity

    def get_equity(self):
        if self.exchange:
            response = self.exchange.fetch_balance(params={"currency":"USDT"})
            if response['info']['code'] == '200000':
                print(response)
                self.equity = response['info']['data']['accountEquity']
                self.balance = response['info']['data']['availableBalance']
                return self.equity
            else:
                print("Problem in getting account equity!")
                print (response)
                return False
        else:
            print("Exchange is not defined!")
            return False

    def get_balance(self):
        if self.exchange:
            response = self.exchange.fetch_balance(params={"currency":"USDT"})
            print(response)
            if response['info']['code'] == '200000':
                self.balance = response['info']['data']['availableBalance']
                self.equity = response['info']['data']['accountEquity']
                return self.balance
            else:
                print("Problem in getting account balance!")
                print (response)
                return False
        else:
            print("Exchange is not defined!")
            return False

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
        numOfLossLong = 0
        numOfLossShort = 0
        for p in closedPositions:
            if p.side == "buy":
                sumOfLongs += p.profit
                numOfLongs += 1
                if p.profit > 0:
                    numOfWinLongs += 1
                    sumOfWinLongs += p.profit
                else:
                    numOfLossLong += 1
                    sumOfLossLongs += p.profit
            else:
                sumOfShorts += p.profit
                numOfShorts += 1
                if p.profit > 0:
                    numOfWinShorts += 1
                    sumOfWinShorts += p.profit
                else:
                    numOfLossShort += 1
                    sumOfLossShorts += p.profit
        if numOfLossShort > 0:
            percentProfitableShorts = numOfWinShorts / numOfLossShort * 100
        else:
            percentProfitableShorts = "infinite"
        if sumOfLossShorts > 0:
            profitFactorShorts = sumOfWinShorts / sumOfLossShorts * -1
        else:
            profitFactorShorts = "infinite"
        if self.numLosses > 0:
            percentProfitable = self.numProfits / self.numLosses * 100
        else:
            percentProfitable = "infinite"
        if numOfLossLong > 0:
            percentProfitableLongs = numOfWinLongs / numOfLossLong * 100
        else:
            percentProfitableLongs = "infinite"
        if sumOfLossLongs > 0:
            profitFactorLongs = sumOfWinLongs / sumOfLossLongs * -1
        else:
            profitFactorLongs = "infinite"
        if self.loss < 0:
            profitFactor = self.profit / self.loss * -1
        else:
            profitFactor = "infinite"
        if len(self.equities) > 0:
            maxDrawDown = self.initialCapital - min(self.equities)
            maxDrawDownPercent = (self.initialCapital - min(self.equities)) / self.initialCapital * 100
        else:
            maxDrawDown = 0
            maxDrawDownPercent = 0
        
        return {
            "netProfit" : self.balance - self.initialCapital,
            "netProfitPercent" : (self.balance - self.initialCapital) / self.initialCapital * 100,
            "netProfitPercentLongs" : sumOfLongs / self.initialCapital * 100,
            "netProfitPercentShorts" : sumOfShorts / self.initialCapital * 100,
            "percentProfitable" : percentProfitable,
            "percentProfitableLongs" : percentProfitableLongs,
            "percentProfitableShorts" : percentProfitableShorts,
            "profitFactor" : profitFactor,
            "profitFactorLongs" : profitFactorLongs,
            "profitFactorShorts" : profitFactorShorts,
            "totalClosedTrades": numOfTrades,
            "totalLongTrades" : numOfLongs,
            "totalShortTrades" : numOfShorts,
            "maxDrawDown": maxDrawDown,
            "maxDrawDownPercent" : maxDrawDownPercent,
        }
