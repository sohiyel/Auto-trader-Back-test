from pprint import isreadable
from data import DataService
from trader import Trader
from userInput import UserInput
import pandas as pd
from pprint import pprint
import time

pair =  "BTC-USDT"
timeFrame = "4hour"
strategyName = "OneEMA"
botName = ""
startAt = "2021-01-01 00:00:00"
endAt = "2021-09-01 00:00:00"
volume = 1
initialCapital = 100000
market = "spot"
optimization = True
randomInputs = False
numberOfInputs = 5

userInput = UserInput(pair, timeFrame, strategyName, botName, optimization, randomInputs)
print("Number of steps: " + str(len(userInput.inputs)))

results = []
if not randomInputs:
    numberOfInputs = len(userInput.inputs)

for i in range(numberOfInputs):
    userInput.step = i
    currentInput = userInput.getCurrentInput()
    
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
    results.append(trader.mainloop())

if optimization:
    results = pd.concat(results)
    timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
    results = results.sort_values(by = 'Net profit per day', ascending = False)
    optimumResult = results.iloc[0]
    # print(optimumResult["TwoEMA_slow_len"])
    userInput.writeOptimizedValues(optimumResult)
    

    print (results)
    if botName:
        path = "optimizations/" + timestr + "_" + pair + "_" + timeFrame + "_" + botName +".csv"
    else:
        path = "optimizations/" + timestr + "_" + pair + "_" + timeFrame + "_" + strategyName +".csv"
    results.to_csv(path)