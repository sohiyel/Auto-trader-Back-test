from pprint import isreadable
from data import DataService
from trader import Trader
from userInput import UserInput
import pandas as pd

# spotData = DataService('spot', "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00")
#futuresData = DataService('futures', ".KXBT", 240, "2021-01-01", "2022-01-01")

"""trader = Trader(market = "spot",
                pair = "ETH-USDT",
                timeFrame = "4hour",
                startAt = "2021-01-01 00:00:00",
                endAt = "2021-09-01 00:00:00",
                initialCapital = 100000,
                strategyName = "RSIStrategy",
                botName= "Bot02",
                volume = 1)"""
# trader = Trader("spot", "BTC-USDT", "1min", "2021-01-01 00:00:00", "2021-01-04 00:00:00", 100000, [])

pair =  "BTC-USDT"
timeFrame = "4hour"
strategyName = "OneEMA"
botName = "Bot01"
startAt = "2021-01-01 00:00:00"
endAt = "2021-09-01 00:00:00"
volume = 1
initialCapital = 100000
market = "spot"
optimization = True

userInput = UserInput(pair, timeFrame, strategyName, botName, optimization)
print("Number of steps: " + str(len(userInput.inputs)))
print(userInput.getCurrentInput())
results = []
for i in range(len(userInput.inputs)):
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
    if botName:
        path = "optimizations/" + pair + "_" + timeFrame + "_" + botName +".csv"
    else:
        path = "optimizations/" + pair + "_" + timeFrame + "_" + strategyName +".csv"
    results.to_csv(path)