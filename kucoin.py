import requests
from tfMap import tfMap

class Kucoin:
    def __init__(self, sandBox=True):
        self.sandBox = sandBox