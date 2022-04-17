from os import path

class Settings:
    constantNumbers = {
        "commission" : 0.0006,
        "data_limit_future" : 200,
        "data_limit_spot" : 1440
    }
    BASE_DIR = path.abspath(path.curdir)
    ACCOUNT_DIR = path.join(BASE_DIR,"account")
    SOURCE_DIR = path.join(BASE_DIR, "src")
    SIGNALS_DIR = path.join(ACCOUNT_DIR, "signals")
    STRATEGIES_DIR = path.join(ACCOUNT_DIR, "strategies")
    REPORTS_DIR = path.join(ACCOUNT_DIR, "reports")
    SETTINGS_DIR = path.join(ACCOUNT_DIR,"settings")
    OPTIMIZATIONS_DIR = path.join(ACCOUNT_DIR, "optimizations")
    DATA_DIR = path.join(ACCOUNT_DIR, "data")
    FUTURE_DATA_DIR = path.join(DATA_DIR, "future")
    SPOT_DATA_DIR = path.join(DATA_DIR, "spot")
    CONFIGURATIONS_DIR = path.join(ACCOUNT_DIR, "configurations")
    API_FUTURE_PATH = path.join(CONFIGURATIONS_DIR, "api_future.cfg")
    API_SANDBOX_FUTURE_PATH = path.join(CONFIGURATIONS_DIR, "api_sandbox_future.cfg")
    API_PATH = path.join(CONFIGURATIONS_DIR, "api.cfg")
    API_SANDBOX_PATH = path.join(CONFIGURATIONS_DIR, "api_sandbox.cfg")
    DB_CONFIG_PATH = path.join(CONFIGURATIONS_DIR, "db.cfg")
    DATABASE_INDEXES_PATH = path.join(SETTINGS_DIR, "database_indexes.json")
    TASKS_PATH = path.join(SETTINGS_DIR,"tasks.json")
    TRADES_PATH = path.join(SETTINGS_DIR, "trades.json")
    MARKET_JSON_PATH = path.join(SETTINGS_DIR, "markets.json")

if __name__ == '__main__':
    print("BASE_DIR: " + Settings.BASE_DIR)
    print("ACCOUNT_DIR: " + Settings.ACCOUNT_DIR)
    print("SOURCE_DIR: " + Settings.SOURCE_DIR)
    print("STRATEGIES_DIR: " + Settings.STRATEGIES_DIR)