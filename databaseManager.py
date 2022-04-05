import psycopg2
import json
import configparser
from tfMap import tfMap
import pandas as pd
import time
class DatabaseManager():
    def __init__(self) -> None:
        self.conn = None
        self.connect_to_db()
        self.tables = []

    def connect_to_db(self):
        try:
            cfg = configparser.ConfigParser()
            cfg.read('db.cfg')
            username = cfg.get('KEYS','user')
            password = cfg.get('KEYS', 'password')
            host = cfg.get('KEYS', 'host')
            port = cfg.get('KEYS', 'port')
            try:
                self.conn = psycopg2.connect(database = "trader", user = username, password = password, host = host, port = port)
            except:
                print ("Unable to connect to the database!")
        except:
            print ("Cannot read db config file!")

    def create_ohlcv_table(self, pair, timeFrame):
        dbPair = tfMap.get_db_format(pair)
        cur = self.conn.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS {} (
                        dt numeric PRIMARY KEY,
                        open numeric NOT NULL,
                        high numeric NOT NULL,
                        low numeric NOT NULL,
                        close numeric NOT NULL,
                        volume numeric NOT NULL
                        );'''.format(dbPair+"_"+timeFrame))
        except:
            print ("Cannot create {} table!".format(dbPair+"_"+timeFrame))

        self.conn.commit()
        cur.close()

    def create_positions_table(self):
        cur = self.conn.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS positions (
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
                        botName text 
                        );''')
        except:
            print ("Cannot create positions table!")

        self.conn.commit()
        cur.close()

    def set_up_tables(self):
        self.tables = []
        with open("settings/database_indexes.json","r") as json_data_file:
            self.jsonFile = json.load(json_data_file)
            ptss = self.jsonFile["tables"]
            for pts in ptss:
                self.tables.append( (pts["pair"], pts["tf"]))
        for i in self.tables:
            self.create_ohlcv_table(i[0], i[1])
        self.create_positions_table()

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
                    print (f"Cannot write this data to {tableName}")
                    print (k)

            self.conn.commit() 
            cur.close()

    def read_klines(self, pair, timeFrame, limit, lastState):
        cur = self.conn.cursor()
        tableName = tfMap.get_db_format(pair) + "_" + timeFrame
        try:
            cur.execute(f"SELECT * FROM {tableName} WHERE dt < {lastState} ORDER BY dt DESC LIMIT {limit};")
            query = cur.fetchall()
            df = pd.DataFrame(query, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'], dtype=float)
            cur.close()
            return df
        except:
            cur.close()
            print (f"Cannot find table {tableName}!")
            query = []
            df = pd.DataFrame(query, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            return df

    def get_open_positions(self, pair):
        cur = self.conn.cursor()
        try:
            SQL = "SELECT * FROM positions WHERE pair = '{0}' AND isopen = True;".format(pair)
            cur.execute(SQL)
            query = cur.fetchall()
            df = pd.DataFrame(query, columns=['id', 'pair', 'side', 'volume', 'entryPrice',
                                                'openAt', 'closeAt', 'leverage', 'isOpen', 'timeFrame',
                                                'strategyName', 'botName'])
            self.conn.commit()
            cur.close()
            return df
        except:
            self.conn.commit()
            cur.close()
            print (f"Cannot get open positions!")
            query = []
            df = pd.DataFrame(query, columns=['id', 'pair', 'side', 'volume', 'entryPrice',
                                             'openAt', 'closeAt', 'leverage, isOpen', 'timeFrame',
                                             'strategyName', 'botName'])
            return df

    def add_position(self, id, pair, side, volume, entryPrice, openAt, leverage, isOpen, timeFrame, strategyName, botName):
        cur = self.conn.cursor()
        try:
            SQL = "INSERT into positions (id, pair, side, volume, entryPrice, openAt, leverage, isOpen, timeFrame, strategyname, botname)\
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data = (id,pair,side,volume,entryPrice,openAt,leverage,isOpen,timeFrame,strategyName,botName)
            cur.execute(SQL, data)
        except:
            print (f"Cannot add new position to database!")

        self.conn.commit() 
        cur.close()

    def close_position(self, id):
        cur = self.conn.cursor()
        # try:
        cur.execute(f"UPDATE positions\
                    SET isopen = False, closeat = {time.time()}\
                    WHERE id='{id}';")
        # except:
        #     print (f"Cannot close position {id}")

        self.conn.commit() 
        cur.close()

if __name__ == '__main__':
    dbManager = DatabaseManager()
    dbManager.set_up_tables()
    dbManager.conn.close()
