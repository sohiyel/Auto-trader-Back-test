from os import path
import json

class Settings:
    def __init__(self,username, task='backtest') -> None:
        self.username = username
        self.task = task
        self.exchange_service = None
        self.exchanges = {1: 'kucoin_futures', 
                        2: 'kucoin_spot',
                        3: 'okex_future',
                        4: 'okex_spot'}

        self.BASE_DIR = path.abspath(path.curdir)
        self.ACCOUNT_DIR = path.join(self.BASE_DIR,"accounts",self.username)
        self.SOURCE_DIR = path.join(self.BASE_DIR, "src")
        self.SIGNALS_DIR = path.join(self.ACCOUNT_DIR, "signals")
        self.STRATEGIES_DIR = path.join(self.ACCOUNT_DIR, "strategies")
        self.REPORTS_DIR = path.join(self.ACCOUNT_DIR, "reports")
        self.SETTINGS_DIR = path.join(self.ACCOUNT_DIR,"settings")
        self.OPTIMIZATIONS_DIR = path.join(self.ACCOUNT_DIR, "optimizations")
        self.DATA_DIR = path.join(self.ACCOUNT_DIR, "data")
        self.FUTURE_DATA_DIR = path.join(self.DATA_DIR, "future")
        self.SPOT_DATA_DIR = path.join(self.DATA_DIR, "spot")
        self.CONFIGURATIONS_DIR = path.join(self.ACCOUNT_DIR, "configurations")
        self.API_FUTURE_PATH = path.join(self.CONFIGURATIONS_DIR, "api_future.cfg")
        self.API_SANDBOX_FUTURE_PATH = path.join(self.CONFIGURATIONS_DIR, "api_sandbox_future.cfg")
        self.API_SANDBOX_PATH = path.join(self.CONFIGURATIONS_DIR, "api_sandbox.cfg")
        self.DB_CONFIG_PATH = path.join(self.CONFIGURATIONS_DIR, "db.cfg")
        self.DATABASE_INDEXES_PATH = path.join(self.SETTINGS_DIR, "database_indexes.json")
        self.TASKS_PATH = path.join(self.SETTINGS_DIR,"tasks.json")
        self.TRADES_PATH = path.join(self.SETTINGS_DIR, "trades.json")
        self.SETTINGS_PATH = path.join(self.SETTINGS_DIR, "settings.json")
        self.MARKET_JSON_PATH = path.join(self.SETTINGS_DIR, "markets.json")
        self.STRATEGIES_MODULE_PATH = f"accounts.{self.username}.strategies."
        self.LOG_FILE = path.join(self.ACCOUNT_DIR, "logs.log")
        self.CSV_DATA = path.join(self.ACCOUNT_DIR,"csv")

        jsonFile = self.load_settings()    
        self.multiProcess = jsonFile["multiProcess"] if "multiProcess" in jsonFile else False
        self.exchange = jsonFile["exchange"] if "exchange" in jsonFile else self.exchanges[1]
        self.tradeSide = jsonFile["tradeSide"] if "tradeSide" in jsonFile else "both"
        self.baseCurrency = jsonFile["baseCurrency"] if "baseCurrency" in jsonFile else "USDT"
        self.sandbox = jsonFile["sandbox"] if "sandbox" in jsonFile else False
        self.constantNumbers = jsonFile["constantNumbers"] if "constantNumbers" in jsonFile else {
                                                                                                    "commission" : 0.0006,
                                                                                                    "data_limit_future" : 200,
                                                                                                    "data_limit_spot" : 1440,
                                                                                                    "max_of_each_pair_margins" : 0.2,
                                                                                                    "free_balance": 0.2,
                                                                                                    "open_position_delays": 3
                                                                                                }
        self.isSpot = True if self.exchange.split('_')[1] == 'spot' else False
        self.tradeSide = self.tradeSide if self.isSpot == False else "long"

        self.API_PATH = {
            False: path.join(self.CONFIGURATIONS_DIR, self.exchange+ ".cfg"), 
            True: path.join(self.CONFIGURATIONS_DIR, self.exchange+ "_sandbox.cfg") 
            }[self.sandbox]

    def load_settings(self):
        try:
            json_data_file = open(self.SETTINGS_PATH,"r")
            jsonFile = json.load(json_data_file)
            json_data_file.close()
            return jsonFile
        except Exception as e:
            print("Cannot read settings json!")
            return {}


if __name__ == '__main__':
    print("BASE_DIR: " + Settings.BASE_DIR)
    print("ACCOUNT_DIR: " + Settings.ACCOUNT_DIR)
    print("SOURCE_DIR: " + Settings.SOURCE_DIR)
    print("STRATEGIES_DIR: " + Settings.STRATEGIES_DIR)