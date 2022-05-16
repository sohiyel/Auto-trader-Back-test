import requests
from src.utility import Utility

class Kucoin:
    def __init__(self, sandBox=False):
        self.sandBox = sandBox