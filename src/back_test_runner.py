from pprint import isreadable
from src.backTest import BackTest
from src.fastBackTest import FastBackTest
from src.userInput import UserInput
import pandas as pd
from pprint import pprint
import time
from datetime import datetime
import concurrent.futures
from src.backTestTask import BackTestTask
from os import path

class BackTestRunner():
    def __init__(self, settings, fast = True) -> None:
        self.settings = settings
        self.multiProcess = settings.multiProcess
        self.task = BackTestTask(self.settings)
        self.userInput = ""
        self.historyNeeded = ""
        self.isFast = fast

    def run_back_test(self, currentInput):
        print  ("--------- New process started ---------")
        self.historyNeeded = self.userInput.calc_history_needed()
        print(f'Number of history needed in secnds: {self.historyNeeded}')
        if self.isFast:
            trader = FastBackTest(market = self.task.market,
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
                        historyNeeded = self.historyNeeded,
                        settings = self.settings)
        else:
            trader = BackTest(market = self.task.market,
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
                            historyNeeded = self.historyNeeded,
                            settings = self.settings)
        result = trader.mainloop()
        print  ("--------- A process has finished! ---------")
        return result

    def start_task(self):
        if self.task.read_toDo():
            self.userInput = UserInput(pair = self.task.pair,
                                  timeFrame = self.task.timeFrame,
                                  strategyName = self.task.strategyName,
                                  botName = self.task.botName,
                                  optimization = self.task.optimization,
                                  randomInput = self.task.randomInputs,
                                  settings = self.settings)
            start_time = time.time()
            print("Number of steps: " + str(len(self.userInput.inputs)))
            results = []
            if not self.task.randomInputs:
                numberOfInputs = len(self.userInput.inputs)
            if self.multiProcess:
                with concurrent.futures.ProcessPoolExecutor() as executer:
                    results = executer.map( self.run_back_test, self.userInput.inputs)
            else:
                for i in self.userInput.inputs:
                    results.append(self.run_back_test(i))
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
            optimizationPath = path.join(self.settings.OPTIMIZATIONS_DIR , timestr + "_" + self.task.pair + "_" + self.task.timeFrame + "_" + self.task.botName +".csv")
        else:
            optimizationPath = path.join(self.settings.OPTIMIZATIONS_DIR , timestr + "_" + self.task.pair + "_" + self.task.timeFrame + "_" + self.task.strategyName +".csv")
        results.to_csv(optimizationPath)
        self.userInput.write_optimized_values(optimumResult)
            
        print("--- End of optimization: {endTime} ---".format(endTime=str(datetime.fromtimestamp(time.time()))))

if __name__ == '__main__':
    
    tradeRunner = BackTestRunner(multiProcess = True)
    while True:
        tradeRunner.start_task()
        time.sleep(5)

