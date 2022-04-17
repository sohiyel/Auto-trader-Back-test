import requests
from src.tfMap import tfMap

class Kucoin:
    def __init__(self, sandBox=False):
        self.sandBox = sandBox