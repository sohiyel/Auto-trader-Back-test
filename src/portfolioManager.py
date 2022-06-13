from src.markets import Markets
from src.logManager import LogService

class PortfolioManager():
    def __init__(self, pair,timeFrame,StrategyName, initialCapital=1, settings="") -> None:
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
        self.exchange = settings.exchange_service #exchange
        self.contractSize = Markets(self.settings).get_contract_size(pair)
        self.logService = LogService(__name__, settings)
        pts = {'pair': pair, 'timeFrame': timeFrame, 'strategyName': StrategyName}
        self.logService.set_pts_formatter(pts)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        
    def calc_poL(self):
        if self.loss != 0:
            self.pol = abs( self.profit / self.loss )

    def open_position(self, volume, price, commission):
        try:
            if volume * float(price) *  ( 1 + commission ) * self.contractSize < self.balance:
                self.balance -= volume * price * self.contractSize
                return True
            else:
                self.logger.warning ("Insufficent balance!", self.balance, price * volume * self.contractSize)
                return False
        except Exception as e:
            self.logger.error("Cannot open position:" + str(e))

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
            self.logger.warning ("Insufficent balance!")
            return False

    def update_equity(self, lastPrice):
        self.equity = self.balance + lastPrice
        return self.equity

    def get_equity(self):
        if self.settings.task == 'trade': #self.exchange:
            try:
                response = self.exchange.fetch_balance()
                if response:
                    self.equity = float(response['Equity'])
                    self.balance = float(response['Balance'])
                    return self.equity
                else:
                    self.logger.error("Problem in getting account equity!")
                    self.logger.error (response)
                    return False
            except Exception as e:
                self.logger.error("Cannot fetch balance from ccxt!"+ str(e))
        else:
            self.logger.error("Exchange is not defined!")
            return False

    # def get_balance(self):
    #     if self.exchange:
    #         try:
    #             response = self.exchange.fetch_balance(params={"currency":"USDT"})
    #             if response['info']['code'] == '200000':
    #                 self.balance = response['info']['data']['availableBalance']
    #                 self.equity = response['info']['data']['accountEquity']
    #                 return self.balance
    #             else:
    #                 self.logger.error("Problem in getting account balance!")
    #                 self.logger.error (response)
    #                 return False
    #         except:
    #             self.logger.error("Cannot fetch balance from ccxt!")
    #     else:
    #         self.logger.error("Exchange is not defined!")
    #         return False

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
            self.logger.warning("Number of loss shorts is zero!")
        if sumOfLossShorts > 0:
            profitFactorShorts = sumOfWinShorts / sumOfLossShorts * -1
        else:
            profitFactorShorts = "infinite"
            self.logger.warning("Number of profit factor shorts is zero!")
        if self.numLosses > 0:
            percentProfitable = self.numProfits / self.numLosses * 100
        else:
            self.logger.warning("Number of losses is zero!")
            percentProfitable = "infinite"
        if numOfLossLong > 0:
            percentProfitableLongs = numOfWinLongs / numOfLossLong * 100
        else:
            self.logger.warning("Number of loss longs is zero!")
            percentProfitableLongs = "infinite"
        if sumOfLossLongs > 0:
            profitFactorLongs = sumOfWinLongs / sumOfLossLongs * -1
        else:
            profitFactorLongs = "infinite"
            self.logger.warning("Sum of loss longs is zero!")
        if self.loss < 0:
            profitFactor = self.profit / self.loss * -1
        else:
            profitFactor = "infinite"
            self.logger.warning("Loss is zero!")
        if len(self.equities) > 0:
            maxDrawDown = self.initialCapital - min(self.equities)
            maxDrawDownPercent = (self.initialCapital - min(self.equities)) / self.initialCapital * 100
        else:
            maxDrawDown = 0
            maxDrawDownPercent = 0
            self.logger.warning("Number of equities is zero!")
        
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
