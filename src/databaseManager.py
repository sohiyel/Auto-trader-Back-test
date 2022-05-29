import psycopg2
import json
import configparser
from src.utility import Utility
import pandas as pd
import time
from src.logManager import LogService
class DatabaseManager():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.conn = None
        self.connect_to_db()
        self.tables = []
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)

    def connect_to_db(self):
        try:
            cfg = configparser.ConfigParser()
            cfg.read(self.settings.DB_CONFIG_PATH)
            username = cfg.get('KEYS','user')
            password = cfg.get('KEYS', 'password')
            host = cfg.get('KEYS', 'host')
            port = cfg.get('KEYS', 'port')
            try:
                self.conn = psycopg2.connect(database = "trader", user = username, password = password, host = host, port = port)
            except:
                self.logger.error ("Unable to connect to the database!")
        except:
            self.logger.error ("Cannot read db config file!")

    def get_ohlcv_table_name(self, pair, timeframe):
        dbPair = Utility.get_db_format(pair)
        return self.settings.exchange + "_" + dbPair + "_" + timeframe

    @property
    def positions_table_name(self):
        return self.settings.exchange + "_positions"

    @property
    def orders_table_name(self):
        return self.settings.exchange + "_orders"

    def create_ohlcv_table(self, pair, timeFrame):
        tableName = self.get_ohlcv_table_name(pair, timeFrame)
        cur = self.conn.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS {} (
                        dt numeric PRIMARY KEY,
                        open numeric NOT NULL,
                        high numeric NOT NULL,
                        low numeric NOT NULL,
                        close numeric NOT NULL,
                        volume numeric NOT NULL
                        );'''.format(tableName))
        except:
            self.logger.warning ("Cannot create {} table!".format(tableName))

        self.conn.commit()
        cur.close()

    def create_positions_table(self):
        tableName = self.positions_table_name
        cur = self.conn.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS {} (
                        id text PRIMARY KEY,
                        pair text NOT NULL,
                        side text NOT NULL,
                        volume numeric NOT NULL,
                        entryPrice numeric NOT NULL,
                        openAt numeric NOT NULL,
                        closeAt numeric,
                        leverage numeric NOT NULL,
                        isOpen boolean NOT NULL,
                        timeFrame text NOT NULL,
                        strategyName text NOT NULL,
                        botName text,
                        stopLossOrderId text,
                        takeProfitOrderId text
                        );'''.format(tableName ))
        except:
            self.logger.warning ("Cannot create {} table!".format(tableName))

        self.conn.commit()
        cur.close()

    def create_orders_table(self):
        tableName = self.orders_table_name
        cur = self.conn.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS {} (
                        id text PRIMARY KEY,
                        pair text NOT NULL,
                        side text NOT NULL,
                        volume numeric NOT NULL,
                        entryPrice numeric NOT NULL,
                        leverage numeric NOT NULL,
                        isOpen boolean NOT NULL,
                        timeFrame text NOT NULL,
                        strategyName text NOT NULL,
                        botName text,
                        positionId text
                        );'''.format(tableName))
        except:
            self.logger.warning ("Cannot create {} table!".format(tableName))

        self.conn.commit()
        cur.close()

    def set_up_tables(self):
        self.tables = []
        with open(self.settings.DATABASE_INDEXES_PATH,"r") as json_data_file:
            self.jsonFile = json.load(json_data_file)
            ptss = self.jsonFile["tables"]
            for pts in ptss:
                self.tables.append( (pts["pair"], pts["tf"]))
        for i in self.tables:
            self.create_ohlcv_table(i[0], i[1])
        self.create_positions_table()
        self.create_orders_table()

    def store_klines(self, klines, tableName):
        for index, k in klines.iterrows():
            cur = self.conn.cursor()
            try:
                cur.execute(f"INSERT into {tableName} (dt, open, high, low, close, volume)\
                            VALUES ({k['timestamp']},{k['open']},{k['high']},{k['low']},{k['close']},{k['volume']});")
            except:
                self.conn.commit() 
                cur.close()
                cur = self.conn.cursor()
                try:
                    cur.execute(f"UPDATE {tableName}\
                                SET open = {k['open']}, high = {k['high']}, low = {k['low']}, close = {k['close']}, volume = {k['volume']}\
                                WHERE dt={k['timestamp']};")
                except:
                    self.logger.error (f"Cannot write this data to {tableName}")

            self.conn.commit() 
            cur.close()

    def read_klines(self, pair, timeFrame, limit, lastState):
        cur = self.conn.cursor()
        tableName = self.get_ohlcv_table_name(pair, timeFrame)
        try:
            cur.execute(f"SELECT * FROM {tableName} WHERE dt < {lastState} ORDER BY dt DESC LIMIT {limit};")
            query = cur.fetchall()
            df = pd.DataFrame(query, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'], dtype=float)
            cur.close()
            return df
        except:
            cur.close()
            self.logger.error (f"Cannot find table {tableName}!")
            query = []
            df = pd.DataFrame(query, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            return df

    def fetch_klines(self, pair, timeFrame, startAt, endAt):
        cur = self.conn.cursor()
        tableName = self.get_ohlcv_table_name(pair, timeFrame)
        try:
            cur.execute(f"SELECT * FROM {tableName} WHERE dt < {endAt + 1} AND dt > {startAt - 1} ORDER BY dt ASC;")
            query = cur.fetchall()
            df = pd.DataFrame(query, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'], dtype=float)
            cur.close()
            return df
        except:
            cur.close()
            self.logger.error (f"Cannot find table {tableName}!")
            query = []
            df = pd.DataFrame(query, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            return df

    def get_open_positions(self, pair):
        tableName = self.positions_table_name
        cur = self.conn.cursor()
        try:
            SQL = "SELECT * FROM {} WHERE pair = '{}' AND isopen = True;".format(tableName, pair)
            cur.execute(SQL)
            query = cur.fetchall()
            df = pd.DataFrame(query, columns=['id', 'pair', 'side', 'volume', 'entryPrice',
                                                'openAt', 'closeAt', 'leverage', 'isOpen', 'timeFrame',
                                                'strategyName', 'botName', 'stopLossOrderId', 'takeProfitOrderId'])
            self.conn.commit()
            cur.close()
            return df
        except:
            self.conn.commit()
            cur.close()
            self.logger.error (f"Cannot get open positions!")
            query = []
            df = pd.DataFrame(query, columns=['id', 'pair', 'side', 'volume', 'entryPrice',
                                             'openAt', 'closeAt', 'leverage, isOpen', 'timeFrame',
                                             'strategyName', 'botName', 'stopLossOrderId', 'takeProfitOrderId'])
            return df

    def get_open_orders(self, pair):
        tableName = self.orders_table_name
        cur = self.conn.cursor()
        try:
            SQL = "SELECT * FROM {} WHERE pair = '{}' AND isopen = True;".format(tableName, pair)
            cur.execute(SQL)
            query = cur.fetchall()
            df = pd.DataFrame(query, columns=['id', 'pair', 'side', 'volume', 'entryPrice', 'leverage', 'isOpen', 'timeFrame',
                                                'strategyName', 'botName', 'positionId'])
            self.conn.commit()
            cur.close()
            return df
        except:
            self.conn.commit()
            cur.close()
            self.logger.error (f"Cannot get open orders!")
            query = []
            df = pd.DataFrame(query, columns=['id', 'pair', 'side', 'volume', 'entryPrice', 'leverage, isOpen', 'timeFrame',
                                             'strategyName', 'botName', 'positionId'])
            return df

    def add_position(self, id, pair, side, volume, entryPrice, openAt, leverage, isOpen, timeFrame, strategyName, botName, stopLossOrderId, takeProfitOrderId):
        tableName = self.positions_table_name
        cur = self.conn.cursor()
        try:
            SQL = "INSERT into %s (id, pair, side, volume, entryPrice, openAt, leverage, isOpen, timeFrame, strategyname, botname, stopLossOrderId, takeProfitOrderId)\
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data = (tableName, id, pair, side, volume, entryPrice, openAt, leverage, isOpen, timeFrame, strategyName, botName, stopLossOrderId, takeProfitOrderId)
            cur.execute(SQL, data)
        except:
            self.logger.error (f"Cannot add new position to database!")

        self.conn.commit() 
        cur.close()

    def add_order(self, id, pair, side, volume, entryPrice, leverage, isOpen, timeFrame, strategyName, botName, positionId):
        tableName = self.orders_table_name
        cur = self.conn.cursor()
        try:
            SQL = "INSERT into %s (id, pair, side, volume, entryPrice, leverage, isOpen, timeFrame, strategyname, botname, positionId)\
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data = (tableName, id, pair, side, volume, entryPrice, leverage, isOpen, timeFrame, strategyName, botName, positionId)
            cur.execute(SQL, data)
        except:
            self.logger.error (f"Cannot add new order to database!")

        self.conn.commit() 
        cur.close()

    def close_position(self, id):
        tableName = self.positions_table_name
        cur = self.conn.cursor()
        try:
            cur.execute(f"UPDATE {tableName}\
                        SET isopen = False, closeat = {time.time()}\
                        WHERE id='{id}';")
        except:
            self.logger.error (f"Cannot close position {id}")

        self.conn.commit() 
        cur.close()

    def close_order(self, id):
        tableName = self.orders_table_name
        cur = self.conn.cursor()
        try:
            cur.execute(f"UPDATE {tableName}\
                        SET isopen = False\
                        WHERE id='{id}';")
        except:
            self.logger.error (f"Cannot close order {id}")

        self.conn.commit() 
        cur.close()

    def close_order_by_positionId(self, id):
        tableName = self.orders_table_name
        cur = self.conn.cursor()
        try:
            cur.execute(f"UPDATE {tableName}\
                        SET isopen = False\
                        WHERE positionId='{id}';")
        except:
            self.logger.error (f"Cannot close order {id}")

        self.conn.commit() 
        cur.close()

if __name__ == '__main__':
    dbManager = DatabaseManager()
    dbManager.set_up_tables()
    dbManager.conn.close()
