from logging import raiseExceptions


class Utility:
    array = {"1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30, "45m": 45, "1h": 60, "3h": 180, "4h": 240, "1d": 60 * 24,
            "1min": 1, "3min": 3, "5min": 5, "15min": 15, "30min": 30, "45min": 45, "1hour": 60, "3hour": 180, "4hour": 240, "1day": 60 * 24,
            "1": 1, "3": 3, "5": 5, "15": 15, "30": 30, "45": 45, "60": 60, "180": 180, "240": 240, "1440": 60 * 24}
    
    @staticmethod
    def get_exchange_format(pair):
        if "/" in pair:
            if ":" in pair:
                return pair.upper()
            else:
                return pair.upper()
        elif "_" in pair:
            pairs = pair.split("_")
            return pairs[0].upper() + "/" + pairs[1].upper()
        elif "-" in pair:
            pairs = pair.split("-")
            return pairs[0].upper() + "/" + pairs[1].upper()

    @staticmethod
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
    
    @staticmethod
    def opposite_side(side):
        if side == 'buy':
            return 'sell'
        elif side == 'sell':
            return 'buy'

    @staticmethod
    def get_stop_side(side):
        if side == 'buy':
            return 'down'
        elif side == 'sell':
            return 'up'

    @staticmethod
    def get_profit_side(side):
        if side == 'buy':
            return 'up'
        elif side == 'sell':
            return 'down'

    @staticmethod
    def truncate(num, n):
        integer = int(num * (10**n))/(10**n)
        return float(integer)


    @staticmethod
    def unify_timeframe(timeframe, exchange):
        num = "".join(filter(str.isdigit, timeframe))
        period = timeframe.replace(num, "")[0]
        return num + period


        if exchange == "kucoinfutures":
            if timeframe == '1m' or timeframe == '1min':
                return '1m'
            elif timeframe == '5m' or timeframe == '5mins' or timeframe == '5min':
                return '5m'
            elif timeframe == '15m' or timeframe == '15mins' or timeframe == '15min':
                return '15m'
            elif timeframe == '30m' or timeframe == '30mins' or timeframe == '30min':
                return '30m'
            elif timeframe == '1h' or timeframe == '1hour':
                return '1h'
            elif timeframe == '4h' or timeframe == '4hours' or timeframe == '4hour':
                return '4h'
            elif timeframe == '1d' or timeframe == '1day':
                return '1d'
            elif timeframe == '1w' or timeframe == '1week':
                return '1w'
            else:
                raise ValueError(f"This timeframe({timeframe}) is not valid in {exchange} exchange!")


