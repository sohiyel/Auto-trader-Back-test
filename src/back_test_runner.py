from src.userInput import UserInput
import pandas as pd
import time
from datetime import datetime
import concurrent.futures
from src.backTestTask import BackTestTask
from os import path
from src.simulator import Simulator
from src.logManager import LogService
from src.databaseManager import DatabaseManager
from random import shuffle
class BackTestRunner():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.multiProcess = settings.multiProcess
        self.task = BackTestTask(self.settings)
        self.userInput = ""
        self.historyNeeded = ""
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)

    def run_back_test(self, currentInput):
        pts = {'pair': self.task.pair, 'timeFrame': self.task.timeFrame, 'strategyName': self.task.strategyName}
        self.logService.set_pts_formatter(pts)
        self.logger.info("--------- New process started ---------")
        self.historyNeeded = self.userInput.calc_history_needed()
        self.logger.info(f'Number of history needed in secnds: {self.historyNeeded}')
        db = DatabaseManager(self.settings, self.task.pair, self.task.timeFrame)
        trader = Simulator(pair = self.task.pair,
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
                    settings = self.settings,
                    db = db)

        result = trader.main_loop()
        self.logger.info  ("--------- A process has finished! ---------")
        return result

    def start_task(self):
        self.task.read_task_file()
        if self.task.read_toDo():
            self.userInput = UserInput(pair = self.task.pair,
                                  timeFrame = self.task.timeFrame,
                                  strategyName = self.task.strategyName,
                                  botName = self.task.botName,
                                  optimization = self.task.optimization,
                                  randomInput = self.task.randomInputs,
                                  settings = self.settings)
            self.userInput.find_inputs()
            start_time = time.time()
            pts = {'pair': self.userInput.pair, 'timeFrame': self.userInput.timeFrame, 'strategyName': self.userInput.strategyName}
            self.logService.set_pts_formatter(pts)
            self.logger.info("Number of steps: " + str(len(self.userInput.inputs)))
            results = []
            shuffle(self.userInput.inputs)
            if self.task.randomInputs:
                numberOfInputs = self.task.numberOfInputs
            else:
                numberOfInputs = len(self.userInput.inputs)
            if self.multiProcess:
                with concurrent.futures.ProcessPoolExecutor() as executer:
                    results = executer.map( self.run_back_test, self.userInput.inputs[:numberOfInputs])
            else:
                for i in range(numberOfInputs):
                    results.append(self.run_back_test(self.userInput.inputs[i]))
            self.task.done_task()
            if self.task.optimization:
                self.write_optimization_output(results)


    def write_optimization_output(self, results):
        results = pd.concat(results)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        results = results.sort_values(by = 'Net profit per day', ascending = False)
        optimumResult = results.iloc[0]
        self.logger.info (results)
        if self.task.botName:
            optimizationPath = path.join(self.settings.OPTIMIZATIONS_DIR , timestr + "_" + self.task.pair + "_" + self.task.timeFrame + "_" + self.task.botName +".csv")
        else:
            optimizationPath = path.join(self.settings.OPTIMIZATIONS_DIR , timestr + "_" + self.task.pair + "_" + self.task.timeFrame + "_" + self.task.strategyName +".csv")
        results.to_csv(optimizationPath)
        self.userInput.write_optimized_values(optimumResult)
            
        self.logger.info("--- End of optimization: {endTime} ---".format(endTime=str(datetime.fromtimestamp(time.time()))))

if __name__ == '__main__':
    
    tradeRunner = BackTestRunner(multiProcess = True)
    while True:
        tradeRunner.start_task()
        time.sleep(5)

