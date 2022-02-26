class ParamInput():
    def __init__(self, name, title, type, value, minValue = 0, maxValue = 0, step = 0, optimization = False) -> None:
        self.name = name
        self.title = title
        self.type = type
        self.value = value
        self.minValue = minValue
        self.maxValue = maxValue
        self.step = step
        self.optimization = optimization
    
        