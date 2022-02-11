class Trader():
    def __init__ (self, pair, startAt, endAt, initialCapital, signalManagers):
        self.pair = pair
        self.startAt = startAt
        self.endAt = endAt
        self.initialCapital = initialCapital
        self.signalManagers = signalManagers