import ccxt
from databaseManager import DatabaseManager
from tfMap import tfMap
from datetime import datetime
from pytz import timezone

class DataDownloader():
    def __init__(self, pair, timeFrame) -> None:
        self.pair = pair
        self.timeFrame = timeFrame
        self.exchange = ccxt.kucoinfutures()
        self.db = DatabaseManager()

    def get_klines(self):
        pair = tfMap.get_exchange_format(self.pair)
        klines = self.exchange.fetch_ohlcv(pair, self.timeFrame)
        print (klines)
        return klines

    def store_klines(self, klines):
        pair = tfMap.get_db_format(self.pair)
        tableName = pair + "_" + self.timeFrame
        cur = self.db.conn.cursor()
        for k in klines:
            dt = datetime.fromtimestamp(k[0]/1000, tz = timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')
            cur.execute(f"INSERT into {tableName} (dt, open, high, low, close, volume) VALUES (TIMESTAMP '{dt}',{k[1]},{k[2]},{k[3]},{k[4]},{k[5]})")

        self.db.conn.commit() 
        cur.close()
        # cur.execute(f"SELECT * FROM {tableName} ORDER BY dt DESC LIMIT 200;")
        # query = cur.fetchall()

if __name__ == '__main__':
    dataDownloader = DataDownloader("BTC_USDT","1m")
    klines = dataDownloader.get_klines()
    dataDownloader.db.create_table("BTC_USDT","1m")
    dataDownloader.store_klines(klines)

