from pprint import isreadable
from data import DataService
from trader import Trader
from userInput import UserInput
import pandas as pd
from pprint import pprint
import time
from datetime import datetime
import concurrent.futures
from tradeTask import TradeTask

class TradeRunner():
    def __init__(self, multiProcess) -> None:
        self.multiProcess = multiProcess
        self.task = TradeTask()
        self.userInput = UserInput(self.task.pair, self.task.timeFrame, self.task.strategyName, self.task.botName, self.task.optimization, self.task.randomInputs)
        self.historyNeeded = self.userInput.calc_history_needed()

    def run_trader(self, currentInput):
        print  ("--------- New process started ---------")
        trader = Trader(market = self.task.market,
                        pair = self.task.pair,
                        timeFrame = self.task.timeFrame,
                        startAt = self.task.startAt,
                        endAt = self.task.endAt,
                        initialCapital = self.task.initialCapital,
                        strategyName = self.task.strategyName,
                        botName= self.task.botName,
                        volume = self.task.volume,
                        currentInput = currentInput,
                        optimization = self.task.optimization,
                        historyNeeded = self.historyNeeded)
        result = trader.mainloop()
        print  ("--------- A process has finished! ---------")
        return result

    def start_task(self):
        if self.task.read_toDo():
            self.userInput = UserInput(self.task.pair, self.task.timeFrame, self.task.strategyName, self.task.botName, self.task.optimization, self.task.randomInputs)
            self.historyNeeded = self.userInput.calc_history_needed()
            print(f'Number of history needed in secnds: {self.historyNeeded}')
            start_time = time.time()
            print("Number of steps: " + str(len(self.userInput.inputs)))
            results = []
            if not self.task.randomInputs:
                numberOfInputs = len(self.userInput.inputs)
            if self.multiProcess:
                with concurrent.futures.ProcessPoolExecutor() as executer:
                    results = executer.map( self.run_trader, self.userInput.inputs)
            else:
                for i in self.userInput.inputs:
                    results.append(self.run_trader(i))
            self.task.done_task()
            if self.task.optimization:
                self.write_optimization_output(results)


    def write_optimization_output(self, results):
        results = pd.concat(results)
        timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
        results = results.sort_values(by = 'Net profit per day', ascending = False)
        optimumResult = results.iloc[0]
        # print(optimumResult["TwoEMA_slow_len"])
        print (results)
        if self.task.botName:
            path = "optimizations/" + timestr + "_" + self.task.pair + "_" + self.task.timeFrame + "_" + self.task.botName +".csv"
        else:
            path = "optimizations/" + timestr + "_" + self.task.pair + "_" + self.task.timeFrame + "_" + self.task.strategyName +".csv"
        results.to_csv(path)
        self.userInput.writeOptimizedValues(optimumResult)
            
        print("--- End of optimization: {endTime} ---".format(endTime=str(datetime.fromtimestamp(time.time()))))

if __name__ == '__main__':
    tradeRunner = TradeRunner(multiProcess = False)
    while True:
        tradeRunner.start_task()
        time.sleep(5)

