from pprint import isreadable
from data import DataService
from trader import Trader
from userInput import UserInput
import pandas as pd
from pprint import pprint
import time
from datetime import datetime
import concurrent.futures

pair =  "BTC-USDT"
timeFrame = "4hour"
strategyName = "RSIStrategy"
botName = "Bot02"
startAt = "2021-01-01 00:00:00"
endAt = "2021-09-01 00:00:00"
volume = 1
initialCapital = 100000
market = "spot"
optimization = True
randomInputs = False
numberOfInputs = 5




def run_trader(currentInput):
    print  ("--------- New process started ---------")
    trader = Trader(market = market,
                    pair = pair,
                    timeFrame = timeFrame,
                    startAt = startAt,
                    endAt = endAt,
                    initialCapital = initialCapital,
                    strategyName = strategyName,
                    botName= botName,
                    volume = volume,
                    currentInput = currentInput,
                    optimization = optimization)
    result = trader.mainloop()
    print  ("--------- A process has finished! ---------")
    return result


start_time = time.time()
userInput = UserInput(pair, timeFrame, strategyName, botName, optimization, randomInputs)
print("Number of steps: " + str(len(userInput.inputs)))

if __name__ == '__main__':
    results = []
    if not randomInputs:
        numberOfInputs = len(userInput.inputs)

    with concurrent.futures.ProcessPoolExecutor() as executer:
        results = executer.map( run_trader, userInput.inputs)
        

    if optimization:
        results = pd.concat(results)
        timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
        results = results.sort_values(by = 'Net profit per day', ascending = False)
        optimumResult = results.iloc[0]
        # print(optimumResult["TwoEMA_slow_len"])
        print (results)
        if botName:
            path = "optimizations/" + timestr + "_" + pair + "_" + timeFrame + "_" + botName +".csv"
        else:
            path = "optimizations/" + timestr + "_" + pair + "_" + timeFrame + "_" + strategyName +".csv"
        results.to_csv(path)
        userInput.writeOptimizedValues(optimumResult)
            
        print("--- End of optimization: {endTime} ---".format(endTime=str(datetime.fromtimestamp(time.time()))))
        print("--- Duration: %s seconds ---" % (time.time() - start_time))
