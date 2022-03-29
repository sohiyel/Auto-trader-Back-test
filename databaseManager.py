import psycopg2
import json
import configparser

class DatabaseManager():
    def __init__(self) -> None:
        self.conn = None
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
                        dt timestamp PRIMARY KEY,
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

if __name__ == '__main__':
    dbManager = DatabaseManager()
    dbManager.connect_to_db()
    dbManager.set_up_tables()
    dbManager.conn.close()
