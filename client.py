import configparser
from kucoin.client import Client

class KucoinClient():
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('api_future.cfg')
        api_key = cfg.get('KEYS','api_key')
        api_secret = cfg.get('KEYS', 'api_secret')
        api_passphrase = cfg.get('KEYS', 'api_passphrase')
        self.client = Client(api_key, api_secret, api_passphrase)