from src.singleStrategy import SingleStrategy
from src.botSignal import BotSignal

class SignalManager():
    def __init__(self, strategyName, botName, currentInput, pair, settings, marketData) -> None:
        if botName == "":
            self.signal = SingleStrategy(strategyName, currentInput, pair, settings, marketData)
        else:
            self.signal = BotSignal(botName = botName,currentInput = currentInput, pair = pair, settings = settings, marketData = marketData)

    def getSignal(self, marketData, timeStamp = ""):
        signal = self.signal.decider(marketData, timeStamp)
        return signal
