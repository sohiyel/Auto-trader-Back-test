from position import Position
import uuid
from databaseManager import DatabaseManager
from tfMap import tfMap
class PositionManager():
    def __init__(self, pair, volume, timeFrame, strategyName, botName, leverage, exchange="") -> None:
        self.openPositions = []
        self.closedPositions = []
        self.pair = pair
        self.volume = volume
        self.timeFrame = timeFrame
        self.strategyName = strategyName
        self.botName = botName
        self.leverage = leverage
        self.exchange = exchange
        self.db = DatabaseManager()
    
    def open_position(self, signal, lastState):
        positionId = uuid.uuid4().hex
        if self.exchange:
            self.exchange.create_market_order(signal.pair, signal.type, signal.volume)
            self.db.add_position(positionId, tfMap.get_db_format(signal.pair), signal.type, self.volume, signal.price, lastState, self.leverage, True, self.timeFrame, self.strategyName, self.botName)
        newPosition = Position(positionId, signal.pair, signal.type, self.volume, signal.price, lastState, self.timeFrame, self.strategyName, self.botName, True, self.leverage, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment)
        self.openPositions.append(newPosition)
        print ( f"-------- Open {signal.type} position on {self.openPositions[0].pair}--------")

    def close_position(self, timestamp):
        if len(self.openPositions) > 0:
            if self.exchange:
                if self.openPositions[0].type == "buy":
                    self.exchange.create_market_order(self.openPositions[0].pair, "sell", self.openPositions[0].volume)
                    print ( f"-------- Close buy position on {self.openPositions[0].pair}--------")
                elif self.openPositions[0].type == "sell":
                    self.exchange.create_market_order(self.openPositions[0].pair, "buy", self.openPositions[0].volume)
                    print ( f"-------- Close sell position on {self.openPositions[0].pair}--------")
                self.db.close_position(self.openPositions[0].id)
            lastPrice = self.openPositions[0].closePosition(timestamp)
            self.closedPositions.append(self.openPositions[0])
            self.openPositions = []
            return lastPrice
        else:
            return

    def add_volume(self, price, volume):
        self.openPositions[0].openPrice = (self.openPositions[0].openPrice * self.openPositions[0].volume + price * volume) / ( self.openPositions[0].volume + volume )
        self.openPositions[0].volume += volume

    def update_positions(self, currentPrice, timestamp):
        for i in self.openPositions:
            i.currentPrice = currentPrice
            i.profit = i.calc_profit()
            if i.type == 'buy':
                if i.takeProfit > 0:
                    if currentPrice > i.takeProfit:
                        return False
                if i.stopLoss > 0:
                    if currentPrice < i.stopLoss:
                        return False
            elif i.type == 'sell':
                if i.takeProfit > 0:
                    if currentPrice < i.takeProfit:
                        return False
                if i.stopLoss > 0:
                    if currentPrice > i.stopLoss:
                        return False
        return True

    def calc_equity(self):
        totalEquity = 0
        for i in self.openPositions:
            totalEquity += i.calc_equity()
        return totalEquity

    def position_average_price(self):
        return 0

    def position_size(self):
        return 0

    def sync_positions(self):
        exchangePositions = self.exchange.fetch_positions()
        dbPositions = self.db.get_open_positions(tfMap.get_db_format(self.pair))
        ep = ""
        for i in exchangePositions:
            if i["symbol"] == tfMap.get_exchange_format(self.pair):
                ep = i
        if ep == "":
            print(f"-------------- There is no position with this pair({self.pair}) in exchange!--------------")
            if len(dbPositions) > 0:
                print(f"-------------- There are some extra position with this pair({self.pair}) in database!--------------")
                for index, k in dbPositions.iterrows():
                    print(f"-------------- Closing position {k['id']} in database! --------------")
                    self.db.close_position(k["id"])
                self.openPositions = []
        else:
            print(f"-------------- There is a position with this pair({self.pair}) in exchange!--------------")
            volumes = 0
            pos = ""
            for index, k in dbPositions.iterrows():
                if k["timeFrame"] == self.timeFrame and k["strategyName"] == self.strategyName and k["botName"] == self.botName:
                    print(f"-------------- There is a position with this pts in database!--------------")
                    pos = k
                volumes += k["volume"]
            if volumes == ep["contractSize"] * 0.001:
                print(f"-------------- Positions in exchange match the positions in database! --------------")
                side = pos["side"]
                if pos["side"] == "long":
                    side = "buy"
                elif pos["side"] == "short":
                    side = "sell"
                positionId = uuid.uuid4().hex
                self.openPositions.append(Position(positionId, pos["symbol"], side, pos["contractSize"] * 1000, pos["entryPrice"], pos["timestamp"], self.timeFrame, self.strategyName, self.botName, True, pos["leverage"]))
                if self.exchange:
                    self.db.add_position(pos["id"], tfMap.get_db_format(pos["symbol"]), side, pos["contractSize"]*1000, pos["entryPrise"], pos["timestamp"], pos["leverage"], True, self.timeFrame, self.strategyName, self.botName)
            else:
                print(f"-------------- Positions in exchange does not match the positions in database! --------------")
                for i in exchangePositions:
                    if i["side"] == "long":
                        self.exchange.create_market_order(i["symbol"], "sell", i["contractSize"]*1000)
                        print ( f"-------- Close buy position on {self.openPositions[0].pair}--------")
                    elif i["side"] == "short":
                        self.exchange.create_market_order(i["symbol"], "buy", i["contractSize"]*1000)
                        print ( f"-------- Close sell position on {self.openPositions[0].pair}--------")