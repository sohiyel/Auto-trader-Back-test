class tfMap:
    array = {"1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30, "45m": 45, "1h": 60, "3h": 180, "4h": 240, "1d": 60 * 24,
            "1min": 1, "3min": 3, "5min": 5, "15min": 15, "30min": 30, "45min": 45, "1hour": 60, "3hour": 180, "4hour": 240, "1day": 60 * 24,
            "1": 1, "3": 3, "5": 5, "15": 15, "30": 30, "45": 45, "60": 60, "180": 180, "240": 240, "1440": 60 * 24}
    
    def get_exchange_format(pair):
        if "/" in pair:
            if ":" in pair:
                return pair.upper()
            else:
                return pair.upper() + ":USDT"
        elif "_" in pair:
            pairs = pair.split("_")
            return pairs[0].upper() + "/" + pairs[1].upper() + ":USDT"
        elif "-" in pair:
            pairs = pair.split("-")
            return pairs[0].upper() + "/" + pairs[1].upper() + ":USDT"

    def get_db_format(pair):
        if "_" in pair:
            if ":" in pair:
                return pair.split(":")[0]
            else:
                return pair
        elif "/" in pair:
            if ":" in pair:
                pair = pair.split(":")[0]
            pairs = pair.split("/")
            return pairs[0] + "_" + pairs[1]
        elif "-" in pair:
            if ":" in pair:
                pair = pair.split(":")[0]
            pairs = pair.split("-")
            return pairs[0] + "_" + pairs[1]

    def opposite_side(side):
        if side == 'buy':
            return 'sell'
        elif side == 'sell':
            return 'buy'

    def get_stop_side(side):
        if side == 'buy':
            return 'down'
        elif side == 'sell':
            return 'up'

    def get_profit_side(side):
        if side == 'buy':
            return 'up'
        elif side == 'sell':
            return 'down'

