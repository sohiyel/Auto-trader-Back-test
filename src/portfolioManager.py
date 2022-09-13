from src.markets import Markets
from src.logManager import LogService

class PortfolioManager():
    def __init__(self, pair,timeFrame,StrategyName, initialCapital=1, settings="") -> None:
        self.settings = settings
        self.logService = LogService(__name__, settings)
        self.exchange = settings.exchange_service #exchange
        pts = {'pair': pair, 'timeFrame': timeFrame, 'strategyName': StrategyName}
        self.pair = pair
        self.logService.set_pts_formatter(pts)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        self.balance = initialCapital
        self.equity = initialCapital
        self.get_equity()
        self.initialCapital = self.balance
        self.profit = 0.0
        self.loss = 0.0
        self.pol = 0.0
        self.numProfits = 0
        self.numLosses = 0
        self.balances = []
        self.equities = []
        self.contractSize = Markets(self.settings).get_contract_size(pair)
        
    def calc_poL(self):
        if self.loss != 0:
            self.pol = abs( self.profit / self.loss )
        else:
            self.pol = "infinite"
        return self.pol

    def open_position(self, volume, price, commission):
        try:
            if self.settings.task == 'trade':
                self.logger.debug("Balance: "+ str(self.balance))
                self.logger.debug("Current order value: "+ str(price * volume))
                self.logger.debug("Balance / Initialcapital: "+str((self.balance - (price * volume)) / self.initialCapital))
                self.logger.debug("Valid free balance: "+ str(self.settings.constantNumbers["free_balance"]))
                if (self.balance - (float(price) * float(volume))) / float(self.initialCapital) < float(self.settings.constantNumbers["free_balance"]):
                    self.logger.debug(f"Not enough free balance to open new order on this pair({self.pair})")
                    return False
        except Exception as e:
            self.logger.error("Cannot check free valid balance: " + str(e))
        try:
            if volume * float(price) *  ( 1 + commission ) * self.contractSize < self.balance:
                self.balance -= volume * price * self.contractSize *  ( 1 + commission )
                return True
            else:
                self.logger.warning ("Insufficent balance!", self.balance, price * volume * self.contractSize)
                return False
        except Exception as e:
            self.logger.error("Cannot open position:" + str(e))

    def close_position(self, lastPrice):
        self.balance += lastPrice

    def add_profit(self, profit):
        if profit > 0 :
            self.profit += profit
            self.numProfits += 1
        else:
            self.logger.error("Profit cannot be lower zero!")
            raise ValueError("Profit cannot be lower zero!")

    def add_loss(self, loss):
        if loss < 0:
            self.loss += loss
            self.numLosses += 1
        else:
            self.logger.error("Loss cannot be above zero!")
            raise ValueError("Loss cannot be above zero!")

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
            self.logger.info("Task in not trade to get equity from exchange!")
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
        loss = 0
        profit = 0
        numLosses = 0
        numProfits = 0
        for p in closedPositions:
            if p.side == "buy":
                sumOfLongs += p.profit
                numOfLongs += 1
                if p.profit > 0:
                    numOfWinLongs += 1
                    sumOfWinLongs += p.profit
                    profit += p.profit
                    numProfits += 1
                else:
                    numOfLossLong += 1
                    sumOfLossLongs += p.profit
                    loss += p.profit
                    numLosses += 1
            else:
                sumOfShorts += p.profit
                numOfShorts += 1
                if p.profit > 0:
                    numOfWinShorts += 1
                    sumOfWinShorts += p.profit
                    profit += p.profit
                    numProfits += 1
                else:
                    numOfLossShort += 1
                    sumOfLossShorts += p.profit
                    loss += p.profit
                    numLosses +=1
        if numOfLossShort > 0:
            percentProfitableShorts = round(numOfWinShorts / numOfLossShort * 100,4)
        else:
            percentProfitableShorts = "infinite"
            self.logger.warning("Number of loss shorts is zero!")
        if sumOfLossShorts != 0:
            profitFactorShorts = round(sumOfWinShorts / sumOfLossShorts * -1,4)
        else:
            profitFactorShorts = "infinite"
            self.logger.warning("Number of profit factor shorts is zero!")
        if numLosses > 0:
            percentProfitable = round(numProfits / numLosses * 100,4)
        else:
            self.logger.warning("Number of losses is zero!")
            percentProfitable = "infinite"
        if numOfLossLong > 0:
            percentProfitableLongs = round(numOfWinLongs / numOfLossLong * 100,4)
        else:
            self.logger.warning("Number of loss longs is zero!")
            percentProfitableLongs = "infinite"
        if sumOfLossLongs != 0:
            profitFactorLongs = round(sumOfWinLongs / sumOfLossLongs * -1,4)
        else:
            profitFactorLongs = "infinite"
            self.logger.warning("Sum of loss longs is zero!")
        if loss < 0:
            profitFactor = round(profit / loss * -1,4)
        else:
            profitFactor = "infinite"
            self.logger.warning("Loss is zero!")
        if len(self.equities) > 0:
            self.logger.debug("min(self.equities):"+str(min(self.equities)))
            maxDrawDown = round(self.initialCapital - min(self.equities),4)
            maxDrawDownPercent = round(((self.initialCapital - min(self.equities)) / self.initialCapital) * 100,4)
        else:
            maxDrawDown = 0
            maxDrawDownPercent = 0
            self.logger.warning("Number of equities is zero!")
        self.logger.debug("InitialCapital:"+str(self.initialCapital))
        self.logger.debug("Balance:"+str(self.balance))
        return {
            "netProfit" : round(self.balance - self.initialCapital,4),
            "netProfitPercent" : round(((self.balance - self.initialCapital) / self.initialCapital) * 100,4),
            "netProfitPercentLongs" : round(sumOfLongs / self.initialCapital * 100,4),
            "netProfitPercentShorts" : round(sumOfShorts / self.initialCapital * 100,4),
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
            "maxDrawDownPercent" : maxDrawDownPercent
        }
