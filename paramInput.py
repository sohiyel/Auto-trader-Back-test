class ParamInput():
    def __init__(self, name, value, strategy, minValue = 0, maxValue = 0, step = 0, optimization = False) -> None:
        self.name = name
        self.value = value
        self.minValue = minValue
        self.maxValue = maxValue
        self.step = step
        self.optimization = optimization
        self.strategy = strategy
    
    def to_dict(self):
        return {
            'name' : self.name,
            'value': self.value,
            'strategy' : self.strategy,
            'minValue': self.minValue,
            'maxValue': self.maxValue,
            'step': self.step,
            'optimization': self.optimization
        }
        