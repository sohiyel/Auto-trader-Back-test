from src.position import Position
import uuid
from src.databaseManager import DatabaseManager
from src.tfMap import tfMap
from src.markets import Markets

class PositionManager():
    def __init__(self, initialCapital, pair, volume, ratioAmount, timeFrame, strategyName, botName, leverage, exchange="") -> None:
        self.openPositions = []
        self.closedPositions = []
        self.initialCapital = initialCapital
        self.pair = pair
        self.volume = volume
        self.ratioAmount = ratioAmount
        self.timeFrame = timeFrame
        self.strategyName = strategyName
        self.botName = botName
        self.leverage = leverage
        self.exchange = exchange
        self.db = DatabaseManager()
        self.contractSize = Markets().get_contract_size(pair)
    
    def open_position(self, signal, lastState):
        positionId = uuid.uuid4().hex
        if self.exchange:
            if self.ratioAmount > 0:
                orderbook = self.exchange.fetch_order_book(signal.pair)
                bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
                ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
                spread = (ask - bid) if (bid and ask) else None
                print('market price', {'bid': bid, 'ask': ask, 'spread': spread})
                amount = 0
                if signal.side == 'buy':
                    amount = self.ratioAmount * self.initialCapital / ask
                elif signal.side == 'sell':
                    amount = self.ratioAmount * self.initialCapital / bid
                volume = amount / self.contractSize
            else:
                volume = self.volume / self.contractSize
                amount = self.volume
                
            self.exchange.create_market_order(signal.pair,
                                                signal.side,
                                                volume,
                                                params={'leverage': self.leverage})
            # stopLossOrderId = self.exchange.create_market_order(signal.pair,
            #                                                     tfMap.opposite_side(signal.side),
            #                                                     volume,
            #                                                     params={'leverage': self.leverage,
            #                                                             'stop': tfMap.get_stop_side(signal.side),
            #                                                             'stopPriceType': 'MP',
            #                                                             'stopPrice': signal.stopLoss})
            # takeProfitOrderId = self.exchange.create_market_order(signal.pair,
            #                                                     tfMap.opposite_side(signal.side),
            #                                                     volume,
            #                                                     params={'leverage': self.leverage,
            #                                                             'stop': tfMap.get_profit_side(signal.side),
            #                                                             'stopPriceType': 'MP',
            #                                                             'stopPrice': signal.takeProfit})
            stopLossOrderId = uuid.uuid4().hex
            takeProfitOrderId = uuid.uuid4().hex
            self.db.add_position(positionId, tfMap.get_db_format(signal.pair), signal.side, amount, signal.price, lastState, self.leverage, True, self.timeFrame, self.strategyName, self.botName, stopLossOrderId, takeProfitOrderId)
            newPosition = Position(positionId, signal.pair, signal.side, amount, signal.price, lastState, self.timeFrame, self.strategyName, self.botName, stopLossOrderId, takeProfitOrderId, True, self.leverage, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment)                
            self.db.add_order(stopLossOrderId, signal.pair, tfMap.opposite_side(signal.side), amount, newPosition.stopLoss, self.leverage, True, self.timeFrame, self.strategyName, self.botName, positionId)
            self.db.add_order(takeProfitOrderId, signal.pair, tfMap.opposite_side(signal.side), amount, newPosition.takeProfit, self.leverage, True, self.timeFrame, self.strategyName, self.botName, positionId)
        else:
            newPosition = Position(positionId, signal.pair, signal.side, self.volume, signal.price, lastState, self.timeFrame, self.strategyName, self.botName, '', '', True, self.leverage, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment)
        self.openPositions.append(newPosition)
        print ( f"-------- Open {signal.side} position on {self.openPositions[0].pair}--------")

    def close_position(self, timestamp):
        if len(self.openPositions) > 0:
            if self.exchange:
                if self.openPositions[0].side == "buy":
                    self.exchange.create_market_order(self.openPositions[0].pair, "sell", self.openPositions[0].volume / self.contractSize, params={'leverage': self.leverage})
                    
                    print ( f"-------- Close buy position on {self.openPositions[0].pair}--------")
                elif self.openPositions[0].side == "sell":
                    self.exchange.create_market_order(self.openPositions[0].pair, "buy", self.openPositions[0].volume / self.contractSize, params={'leverage': self.leverage})
                    print ( f"-------- Close sell position on {self.openPositions[0].pair}--------")
                self.db.close_position(self.openPositions[0].id)
                self.db.close_order_by_positionId(self.openPositions[0].id)
            lastPrice = self.openPositions[0].close_position(timestamp)
            self.closedPositions.append(self.openPositions[0])
            self.openPositions = []
            return lastPrice
        else:
            return

    def add_volume(self, price, volume):
        self.openPositions[0].entryPrice = (self.openPositions[0].entryPrice * self.openPositions[0].volume + price * volume) / ( self.openPositions[0].volume + volume )
        self.openPositions[0].volume += volume

    def update_positions(self, currentPrice, timestamp):
        for i in self.openPositions:
            i.currentPrice = currentPrice
            i.profit = i.calc_profit()
            if i.side == 'buy':
                if i.takeProfit > 0:
                    if currentPrice > i.takeProfit:
                        return False
                if i.stopLoss > 0:
                    if currentPrice < i.stopLoss:
                        return False
            elif i.side == 'sell':
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
        print(exchangePositions)
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
                    self.db.close_order_by_positionId(k["id"])
                self.openPositions = []
        else:
            print(f"-------------- There is a position with this pair({self.pair}) in exchange!--------------")
            volumes = 0
            pos = ""
            for index, k in dbPositions.iterrows():
                if k["timeFrame"] == self.timeFrame:
                    print(f"-------------- There is a position with this pts in database!--------------")
                    pos = k
                volumes += k["volume"]
            print(volumes, ep["contractSize"] * ep["contracts"])
            if float(volumes) == float(ep["contractSize"] * ep["contracts"]) and self.leverage == ep["leverage"]:
                print(f"-------------- Positions in exchange match the positions in database! --------------")
                side = pos["side"]
                if pos["side"] == "long":
                    side = "buy"
                elif pos["side"] == "short":
                    side = "sell"
                positionId = uuid.uuid4().hex
                self.openPositions.append(Position(positionId, ep["symbol"], side, ep["contractSize"] * ep["contracts"], ep["entryPrice"], ep["timestamp"], self.timeFrame, self.strategyName, self.botName, pos["stopLossOrderId"], pos["takeProfitOrderId"], True, ep["leverage"]))
            else:
                print(f"-------------- Positions in exchange does not match the positions in database! --------------")
                for i in exchangePositions:
                    if i["side"] == "long":
                        self.exchange.create_market_order(i["symbol"], "sell", i["contracts"], params={'leverage': self.leverage})
                        print ( f"-------- Close buy position on {i['symbol']}--------")
                    elif i["side"] == "short":
                        self.exchange.create_market_order(i["symbol"], "buy", i["contracts"], params={'leverage': self.leverage})
                        print ( f"-------- Close sell position on {i['symbol']}--------")
                for index, k in dbPositions.iterrows():
                    print(f"-------------- Closing position {k['id']} in database! --------------")
                    self.db.close_position(k["id"])
                    self.db.close_order_by_positionId(k["id"])
                self.openPositions = []