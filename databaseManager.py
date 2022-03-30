import psycopg2
import json
import configparser

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

    def create_table(self, pair, timeFrame):
        cur = self.conn.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS {} (
                        dt numeric PRIMARY KEY,
                        open numeric NOT NULL,
                        high numeric NOT NULL,
                        low numeric NOT NULL,
                        close numeric NOT NULL,
                        volume numeric NOT NULL
                        );'''.format(pair+"_"+timeFrame))
        except:
            print ("Cannot create {} table!".format(pair+"_"+timeFrame))

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
            self.create_table(i[0], i[1])

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

if __name__ == '__main__':
    dbManager = DatabaseManager()
    dbManager.set_up_tables()
    dbManager.conn.close()
