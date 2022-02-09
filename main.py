from client import KucoinClient
from data import DataService

newClient = KucoinClient()
client = newClient.client
d = DataService(client, "BTC-USDT", "1min", "2021-01-01", "2021-01-04")