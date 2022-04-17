import configparser
from kucoin.client import Client
from account.settings.settings import Settings

class KucoinClient():
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read(Settings.API_FUTURE_PATH)
        api_key = cfg.get('KEYS','api_key')
        api_secret = cfg.get('KEYS', 'api_secret')
        api_passphrase = cfg.get('KEYS', 'api_passphrase')
        self.client = Client(api_key, api_secret, api_passphrase)