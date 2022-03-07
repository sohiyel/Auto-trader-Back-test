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

multiProcess = False

tradeTask = TradeTask()
tradeTask.read_toDo()

def run_trader(currentInput):
    print  ("--------- New process started ---------")
    trader = Trader(market = tradeTask.market,
                    pair = tradeTask.pair,
                    timeFrame = tradeTask.timeFrame,
                    startAt = tradeTask.startAt,
                    endAt = tradeTask.endAt,
                    initialCapital = tradeTask.initialCapital,
                    strategyName = tradeTask.strategyName,
                    botName= tradeTask.botName,
                    volume = tradeTask.volume,
                    currentInput = currentInput,
                    optimization = tradeTask.optimization)
    result = trader.mainloop()
    print  ("--------- A process has finished! ---------")
    return result


start_time = time.time()
userInput = UserInput(tradeTask.pair, tradeTask.timeFrame, tradeTask.strategyName, tradeTask.botName, tradeTask.optimization, tradeTask.randomInputs)
print("Number of steps: " + str(len(userInput.inputs)))

if __name__ == '__main__':
    results = []
    if not tradeTask.randomInputs:
        numberOfInputs = len(userInput.inputs)
    if multiProcess:
        with concurrent.futures.ProcessPoolExecutor() as executer:
            results = executer.map( run_trader, userInput.inputs)
    else:
        for i in userInput.inputs:
            results.append(run_trader(i))
        

    if tradeTask.optimization:
        results = pd.concat(results)
        timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
        results = results.sort_values(by = 'Net profit per day', ascending = False)
        optimumResult = results.iloc[0]
        # print(optimumResult["TwoEMA_slow_len"])
        print (results)
        if tradeTask.botName:
            path = "optimizations/" + timestr + "_" + tradeTask.pair + "_" + tradeTask.timeFrame + "_" + tradeTask.botName +".csv"
        else:
            path = "optimizations/" + timestr + "_" + tradeTask.pair + "_" + tradeTask.timeFrame + "_" + tradeTask.strategyName +".csv"
        results.to_csv(path)
        userInput.writeOptimizedValues(optimumResult)
            
        print("--- End of optimization: {endTime} ---".format(endTime=str(datetime.fromtimestamp(time.time()))))
        print("--- Duration: %s seconds ---" % (time.time() - start_time))
        tradeTask.done_task()
