class ParamInput():
    def __init__(self, name, value, strategy, historyNeeded, minValue = 0, maxValue = 0, step = 0, optimization = False) -> None:
        self.name = name
        self.value = value
        self.minValue = minValue
        self.maxValue = maxValue
        self.step = step
        self.optimization = optimization
        self.strategy = strategy
        self.historyNeeded = historyNeeded

    def __eq__(self, other):
        if not isinstance(other, ParamInput):
            return NotImplemented
        return self.name == other.name and self.value == other.value and\
            self.minValue == other.minValue and self.maxValue == other.maxValue and\
                self.step == other.step and self.optimization == other.optimization and\
                    self.strategy == other.strategy and self.optimization == other.optimization and\
                        self.historyNeeded == other.historyNeeded

    def __repr__(self):
        print(self.to_dict())
    
    def to_dict(self):
        return {
            'name' : self.name,
            'value': self.value,
            'strategy' : self.strategy,
            'historyNeeded' : self.historyNeeded
        }
        