from logging import currentframe
import pandas as pd
from positionManager import PositionManager
from orderManager import OrderManager
from data import DataService
from portfolioManager import PortfolioManager
from tfMap import tfMap
from datetime import datetime
from pytz import timezone
import os
from plotter import Plotter
import time


class Trader():
    def __init__ (self,market, pair, timeFrame, startAt, endAt, initialCapital, strategyName, botName, volume, currentInput, optimization):
        self.pair = pair
        self.dataService = DataService(market, pair, timeFrame, startAt, endAt)
        self.startAt = startAt,
        self.endAt = endAt,
        self.startAtTS = self.dataService.startAtTs
        self.endAtTS = self.dataService.endAtTs
        self.lastState = self.dataService.startAtTs
        self.initialCapital = initialCapital
        self.strategyName = strategyName
        self.botName = botName
        self.orderManager = OrderManager(initialCapital, strategyName, botName, currentInput, pair)
        self.positionManager = PositionManager()
        self.portfolioManager = PortfolioManager(initialCapital)
        self.timeFrame = timeFrame
        self.plotter =  Plotter(self.pair + "_" + str(self.startAtTS) + "_" + str(self.endAtTS) + "_" + self.timeFrame + ".csv" )
        self.lastCandle = ""
        self.volume = volume
        self.currentInput = currentInput
        self.optimization = optimization


    def openPosition(self, signal, commission):
        if len( self.positionManager.openPositions ) == 0:
            if self.portfolioManager.openPosition(signal.volume, signal.price, commission):
                self.positionManager.openPosition(signal, self.lastState)
        elif len( self.positionManager.openPositions ) == 1:
            if self.positionManager.openPositions[0].type == signal.type:
                if self.portfolioManager.addVolume(signal.volume, signal.price, commission):
                    self.positionManager.addVolume(signal.price, signal.volume)
            else:
                lastPrice = self.positionManager.closePosition(self.lastState)
                self.portfolioManager.closePosition(lastPrice, commission)
                if self.positionManager.closedPositions[-1].profit > 0:
                    self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
                else:
                    self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
                
                self.portfolioManager.balances.append(self.portfolioManager.balance)
                if self.portfolioManager.openPosition(signal.volume, signal.price, commission):
                    self.positionManager.openPosition(signal, self.lastState)
                

    def closePosition(self, commission):
        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.closePosition(self.lastState)
            self.portfolioManager.closePosition(lastPrice, commission)
            if self.positionManager.closedPositions[-1].profit > 0:
                self.portfolioManager.addProfit(self.positionManager.closedPositions[-1].profit)
            else:
                self.portfolioManager.addLoss(self.positionManager.closedPositions[-1].profit)
            self.portfolioManager.balances.append(self.portfolioManager.balance)

    def processOrders(self, choice, signal, commission ):
        if choice == 0:
            pass

        elif choice == 1:
            if signal:
                self.openPosition(signal, commission)
            
        elif choice == 2:
            self.closePosition(commission)

        elif choice == 3:
            if signal:
                self.openPosition(signal, commission)
            
        elif choice == 4:
            self.closePosition(commission)

        if len(self.positionManager.openPositions) > 0:
            lastPrice = self.positionManager.calcEquity()
            self.portfolioManager.equities.append(self.portfolioManager.updateEquity(lastPrice))



    def mainloop(self):
        global balances
        start_time = time.time()
        print("--- Start time: {startTime} ---".format(startTime=str(datetime.fromtimestamp(time.time()))))
        for i in range(self.dataService.startAtTs,self.dataService.endAtTs, tfMap.array[self.timeFrame]*60):
            if self.portfolioManager.equity <= 0:
                self.processOrders(4, None, 0.0006)
                self.portfolioManager.balance = 0
                break
            self.lastState = i
            self.lastCandle = self.dataService.getCurrentData(i)
            # print(self.lastCandle['close'].values[0])
            checkContinue = self.positionManager.updatePositions(self.lastCandle['close'].values[0], self.lastState)
            if not checkContinue :
                self.processOrders(4, None, 0.00060)
                continue

            choice, signal = self.orderManager.decider(self.lastCandle.iloc[0], self.portfolioManager.equity, self.portfolioManager.balance, self.positionManager.positionAveragePrice(), self.positionManager.positionSize())
            self.processOrders(choice, signal, 0.00060)
            # print(self.portfolioManager.balance)

            self.portfolioManager.calcPoL()

            # clear = lambda: os.system('cls')
            # clear()

            # df = pd.DataFrame.from_records([position.to_dict() for position in self.positionManager.openPositions])
            # df['Balance'] = self.portfolioManager.balance
            # df['Equity'] = self.portfolioManager.equity
            # print(df)

        self.processOrders(4, None, 0.0006)

        report = self.portfolioManager.report(self.positionManager.closedPositions)
        numberOfDays = ((self.endAtTS - self.startAtTS)/(1440 * 60))
        buyAndHold = self.dataService.dataFrame.iloc[-1]["close"] - self.dataService.dataFrame.iloc[0]["close"]
        sellAndHold = buyAndHold * -1
        reportDict = {
                "Net profit percent" : [report["netProfitPercent"]],
                "Net profit per day" : [report["netProfitPercent"] / numberOfDays],
                "Net profit percent long" : [report["netProfitPercentLongs"]],
                "Net profit percent long per day" : [report["netProfitPercentLongs"] / numberOfDays],
                "Net profit percent short" : [report["netProfitPercentShorts"]],
                "Net profit percent short per day" : [report["netProfitPercentShorts"] / numberOfDays],
                "Percent profitable" : [report["percentProfitable"]],
                "Percent profitable long" : [report["percentProfitableLongs"]],
                "Percent profitable short" : [report["percentProfitableShorts"]],
                "Profit factor" : [report["profitFactor"]],
                "Profit factor long" : [report["profitFactorLongs"]],
                "Profit factor short" : [report["profitFactorShorts"]],
                "Number of trades" : [report["totalClosedTrades"]],
                "Number of long trades" : [report["totalLongTrades"]],
                "Number of short trades" : [report["totalShortTrades"]],
                "Maximum drawdown" : [report["maxDrawDown"]],
                "Maximum drawdown percent" : [report["maxDrawDownPercent"]],
                "Number of win trade" : [self.portfolioManager.numProfits],
                "Number of lose trades" : [self.portfolioManager.numLosses],
                "Sum amount of profits" : [self.portfolioManager.profit],
                "Sum amount of loss" : [self.portfolioManager.loss],
                "Current Balance" : [self.portfolioManager.balance],
                "Min of equity" : [min(self.portfolioManager.equities)],
                "Min of balance" : [min(self.portfolioManager.balances)],
                "Number of days per trade" : [numberOfDays / report["netProfitPercent"]],
                "Buy and hold return" : [buyAndHold],
                "Buy and hold return percent" : [buyAndHold / self.initialCapital * 100],
                "Buy and hold return percent per day" : [buyAndHold / self.initialCapital * 100 / numberOfDays],
                "Sell and hold return" : [sellAndHold],
                "Sell and hold return percent" : [sellAndHold / self.initialCapital * 100],
                "Sell and hold return percent per day" : [sellAndHold / self.initialCapital * 100 / numberOfDays],
                "Net profit / Buy and hold" : [report["netProfit"] / buyAndHold],
                "Net profit / Sell and hold" : [report["netProfit"] / sellAndHold],
                "Start time" : self.startAt,
                "End time" : self.endAt,
                "Duration" : numberOfDays
            }

        if self.botName:
            for i in self.currentInput:
                for pi in i:
                    reportDict[pi.strategy + "_" +pi.name] = pi.value
        else:
            for pi in self.currentInput:
                reportDict[pi.name] = pi.value
        result = pd.DataFrame(
            reportDict
        )

        print(result)

        if not self.optimization:
            df = pd.DataFrame.from_records([position.to_dict() for position in self.positionManager.closedPositions])
            df['Balance'] = self.portfolioManager.balances
            print(df)

            self.plotter.writeDFtoFile(df)
        print("--- End time: {endTime} ---".format(endTime=str(datetime.fromtimestamp(time.time()))))
        print("--- Duration: %s seconds ---" % (time.time() - start_time))
        return result

