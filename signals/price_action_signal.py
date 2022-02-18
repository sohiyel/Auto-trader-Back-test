from strategies.price_action01 import PriceAction01

class PriceActionSignal():
    def __init__(self) -> None:
        super().__init__()
        self.lastSignal = 0
        self.marketData = []
        
    def decider(self, marketData):
        self.marketData.append(marketData)
        if len(self.marketData) < 5:
            return 0
        strategy = PriceAction01()
        decision = strategy.decider(self.marketData)
        # print(decision)
        if self.lastSignal == 0 or self.lastSignal == 2 or self.lastSignal == 4:
            if decision['longEnt'] and not decision['shortEnt']:
                self.lastSignal = 1
                return 1
            elif decision['shortEnt'] and not decision['longEnt']:
                self.lastSignal = 3
                return 3
            self.lastSignal = 0
            return 0
        elif self.lastSignal == 1:
            if decision['shortEnt']:
                self.lastSignal = 3
                return 3
            elif decision['longExt']:
                self.lastSignal = 2
                return 2
            return 0
        elif self.lastSignal == 3:
            if decision['longEnt']:
                self.lastSignal = 1
                return 1
            elif decision['shortExt']:
                self.lastSignal = 4
                return 4
            return 0


