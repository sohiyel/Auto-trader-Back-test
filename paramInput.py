class ParamInput():
    def __init__(self, name, title, type, value, minValue = 0, maxValue = 0, step = 0, optimization = False, strategy = "") -> None:
        self.name = name
        self.title = title
        self.type = type
        self.value = value
        self.minValue = minValue
        self.maxValue = maxValue
        self.step = step
        self.optimization = optimization
        self.strategy = strategy
    
    def to_dict(self):
        return {
            'name' : self.name,
            'title': self.title,
            'type': self.type,
            'value': self.value,
            'minValue': self.minValue,
            'maxValue': self.maxValue,
            'step': self.step,
            'optimization': self.optimization,
            'strategy' : self.strategy
        }
        