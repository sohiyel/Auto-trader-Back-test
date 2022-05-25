from os import path

class Settings:
    def __init__(self,username, task='backtest') -> None:
        self.username = username
        self.task = task
        self.multiProcess = False
        self.tradeSide = "both"
        self.exchange = "okex"
        self.sandbox = False
        self.constantNumbers = {
            "commission" : 0.0006,
            "data_limit_future" : 200,
            "data_limit_spot" : 1440
        }
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
        
        self.API_PATH = {
            False: path.join(self.CONFIGURATIONS_DIR, self.exchange+ ".cfg"), 
            True: path.join(self.CONFIGURATIONS_DIR, self.exchange+ "_sandbox.cfg") 
            }[self.sandbox]

        self.API_SANDBOX_PATH = path.join(self.CONFIGURATIONS_DIR, "api_sandbox.cfg")
        self.DB_CONFIG_PATH = path.join(self.CONFIGURATIONS_DIR, "db.cfg")
        self.DATABASE_INDEXES_PATH = path.join(self.SETTINGS_DIR, "database_indexes.json")
        self.TASKS_PATH = path.join(self.SETTINGS_DIR,"tasks.json")
        self.TRADES_PATH = path.join(self.SETTINGS_DIR, "trades.json")
        self.MARKET_JSON_PATH = path.join(self.SETTINGS_DIR, "markets.json")
        self.STRATEGIES_MODULE_PATH = f"accounts.{self.username}.strategies."
        self.LOG_FILE = path.join(self.ACCOUNT_DIR, "logs.log")

if __name__ == '__main__':
    print("BASE_DIR: " + Settings.BASE_DIR)
    print("ACCOUNT_DIR: " + Settings.ACCOUNT_DIR)
    print("SOURCE_DIR: " + Settings.SOURCE_DIR)
    print("STRATEGIES_DIR: " + Settings.STRATEGIES_DIR)