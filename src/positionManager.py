from shutil import ExecError
from src.position import Position
import uuid
from src.databaseManager import DatabaseManager
from src.utility import Utility
from src.markets import Markets
from src.logManager import LogService

class PositionManager():
    def __init__(self, initialCapital, pair, volume, ratioAmount, timeFrame, strategyName, botName, leverage, settings) -> None:
        self.openPositions = []
        self.closedPositions = []
        self.initialCapital = initialCapital
        self.exchange = settings.exchange_service #exchange
        self.pair = self.exchange.change_symbol_for_trade(pair)
        self.volume = volume
        self.ratioAmount = ratioAmount
        self.timeFrame = timeFrame
        self.strategyName = strategyName
        self.botName = botName
        self.leverage = leverage
        
        self.settings = settings
        self.db = DatabaseManager(settings, self.pair, self.timeFrame)
        self.contractSize = Markets(settings).get_contract_size(pair)
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        pts = {'pair': self.pair, 'timeFrame': self.timeFrame, 'strategyName': self.strategyName}
        self.logService.set_pts_formatter(pts)
    
    def open_position(self, signal, lastState):
        positionId = uuid.uuid4().hex
        if self.settings.task == 'trade': #self.exchange:
            if self.ratioAmount > 0:
                orderbook = self.exchange.fetch_order_book(signal.pair)
                bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
                ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
                spread = (ask - bid) if (bid and ask) else None
                self.logger.debug('market price', {'bid': bid, 'ask': ask, 'spread': spread})
                amount = 0
                if signal.side == 'buy':
                    amount = self.ratioAmount * self.initialCapital / ask
                elif signal.side == 'sell':
                    amount = self.ratioAmount * self.initialCapital / bid
                volume = amount / self.contractSize
            else:
                volume = self.volume / self.contractSize
                amount = self.volume
            try:
                if signal.side == 'buy':
                    self.exchange.create_market_order(self.pair,
                                                        signal.side,
                                                        volume,
                                                        self.leverage,
                                                        'open_buy')
                elif signal.side == 'sell':
                    self.exchange.create_market_order(self.pair,
                                                        signal.side,
                                                        volume,
                                                        self.leverage,
                                                        'open_sell')
            except Exception as e:
                self.logger.error("Cannot create market order!" + str(e))
            # stopLossOrderId = self.exchange.create_market_order(signal.pair,
            #                                                     Utility.opposite_side(signal.side),
            #                                                     volume,
            #                                                     params={'leverage': self.leverage,
            #                                                             'stop': Utility.get_stop_side(signal.side),
            #                                                             'stopPriceType': 'MP',
            #                                                             'stopPrice': signal.stopLoss})
            # takeProfitOrderId = self.exchange.create_market_order(signal.pair,
            #                                                     Utility.opposite_side(signal.side),
            #                                                     volume,
            #                                                     params={'leverage': self.leverage,
            #                                                             'stop': Utility.get_profit_side(signal.side),
            #                                                             'stopPriceType': 'MP',
            #                                                             'stopPrice': signal.takeProfit})
            stopLossOrderId = uuid.uuid4().hex
            takeProfitOrderId = uuid.uuid4().hex
            try:
                self.db.add_position(positionId, Utility.get_db_format(signal.pair), signal.side, amount, signal.price, lastState, self.leverage, True, self.timeFrame, self.strategyName, self.botName, stopLossOrderId, takeProfitOrderId)
            except:
                self.logger.error("Cannot add new position to db!")
            newPosition = Position(positionId, signal.pair, signal.side, amount, signal.price, lastState, self.timeFrame, self.strategyName, self.botName, stopLossOrderId, takeProfitOrderId, True, self.leverage, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment, self.settings)                
            try:
                self.db.add_order(stopLossOrderId, signal.pair, Utility.opposite_side(signal.side), amount, newPosition.stopLoss, self.leverage, True, self.timeFrame, self.strategyName, self.botName, positionId)
                self.db.add_order(takeProfitOrderId, signal.pair, Utility.opposite_side(signal.side), amount, newPosition.takeProfit, self.leverage, True, self.timeFrame, self.strategyName, self.botName, positionId)
            except:
                self.logger.error("Cannot add new order to db!")
        else:
            newPosition = Position(positionId, signal.pair, signal.side, self.volume, signal.price, lastState, self.timeFrame, self.strategyName, self.botName, '', '', True, self.leverage, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment, self.settings)
        self.openPositions.append(newPosition)
        self.logger.info ( f"-------- Open {signal.side} position on {self.openPositions[0].pair}--------")

    def close_position(self, timestamp):
        if len(self.openPositions) > 0:
            if self.settings.task == 'trade': #self.exchange:
                if self.openPositions[0].side == "buy":
                    try:
                        self.exchange.create_market_order(self.exchange.change_symbol_for_trade(self.openPositions[0].pair), "sell", self.openPositions[0].volume / self.contractSize,self.leverage, 'close_buy')
                        self.logger.info ( f"-------- Close buy position on {self.openPositions[0].pair}--------")
                    except Exception as e:
                        self.logger.error("Cannot create market order!" + str(e))
                elif self.openPositions[0].side == "sell":
                    try:
                        self.exchange.create_market_order(self.exchange.change_symbol_for_trade(self.openPositions[0].pair), "buy", self.openPositions[0].volume / self.contractSize,self.leverage, 'close_sell')
                        self.logger.info ( f"-------- Close sell position on {self.openPositions[0].pair}--------")
                    except Exception as e:
                        self.logger.error("Cannot create market order!" + str(e))
                try:
                    self.db.close_position(self.openPositions[0].id)
                except:
                    self.logger.error("Cannot close position by id!")
                try:
                    self.db.close_order_by_positionId(self.openPositions[0].id)
                except:
                    self.logger.error("Cannot close order by id!")
            lastPrice = self.openPositions[0].close_position(timestamp)
            self.closedPositions.append(self.openPositions[0])
            self.openPositions = []
            return lastPrice
        else:
            return

    def add_volume(self, price, volume):
        self.openPositions[0].entryPrice = (self.openPositions[0].entryPrice * self.openPositions[0].volume + price * volume) / ( self.openPositions[0].volume + volume )
        self.openPositions[0].volume += volume

    def check_sl_tp(self, currentPrice, timestamp):
        for i in self.openPositions:
            i.currentPrice = currentPrice
            i.profit = i.calc_profit()
            if i.side == 'buy':
                if i.takeProfit > 0:
                    if currentPrice > i.takeProfit:
                        self.logger.info("TP has hitted!")
                        self.logger.info("Side: Buy")
                        self.logger.info(f"Current Price:{currentPrice}")
                        self.logger.info(f"Take Proft:{i.takeProfit}")
                        return False
                if i.stopLoss > 0:
                    if currentPrice < i.stopLoss:
                        self.logger.info("Sl has hitted!")
                        self.logger.info("Side: Buy")
                        self.logger.info(f"Current Price:{currentPrice}")
                        self.logger.info(f"Stop Loss:{i.stopLoss}")
                        return False
            elif i.side == 'sell':
                if i.takeProfit > 0:
                    if currentPrice < i.takeProfit:
                        self.logger.info("TP has hitted!")
                        self.logger.info("Side: Sell")
                        self.logger.info(f"Current Price:{currentPrice}")
                        self.logger.info(f"Take Proft:{i.takeProfit}")
                        return False
                if i.stopLoss > 0:
                    if currentPrice > i.stopLoss:
                        self.logger.info("SL has hitted!")
                        self.logger.info("Side: Sell")
                        self.logger.info(f"Current Price:{currentPrice}")
                        self.logger.info(f"Take Proft:{i.stopLoss}")
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
        dbPositions = self.db.get_open_positions(Utility.get_db_format(self.pair))
        ep = ""
        for i in exchangePositions:
            if i["symbol"] == self.exchange.change_symbol_for_trade(self.pair):
                ep = i
        if ep == "":
            self.logger.info(f"-------------- There is no position with this pair({self.pair}) in exchange!--------------")
            if len(dbPositions) > 0:
                self.logger.info(f"-------------- There are some extra position with this pair({self.pair}) in database!--------------")
                for index, k in dbPositions.iterrows():
                    self.logger.info(f"-------------- Closing position {k['id']} in database! --------------")
                    self.db.close_position(k["id"])
                    self.db.close_order_by_positionId(k["id"])
                self.openPositions = []
        else:
            self.logger.info(f"-------------- There is a position with this pair({self.pair}) in exchange!--------------")
            volumes = 0
            pos = ""
            for index, k in dbPositions.iterrows():
                if k["timeFrame"] == self.timeFrame:
                    self.logger.info(f"-------------- There is a position with this pts in database!--------------")
                    pos = k
                volumes += k["volume"]
            if float(volumes) == float(ep["contractSize"] * ep["contracts"]) and self.leverage == ep["leverage"]:
                self.logger.info(f"-------------- Positions in exchange match the positions in database! --------------")
                side = pos["side"]
                if pos["side"] == "long":
                    side = "buy"
                elif pos["side"] == "short":
                    side = "sell"
                positionId = uuid.uuid4().hex
                self.openPositions.append(Position(positionId, ep["symbol"], side, ep["contractSize"] * ep["contracts"], ep["entryPrice"], ep["timestamp"], self.timeFrame, self.strategyName, self.botName, pos["stopLossOrderId"], pos["takeProfitOrderId"], True, ep["leverage"],settings=self.settings))
            else:
                self.logger.warning(f"-------------- Positions in exchange does not match the positions in database! --------------")
                for i in exchangePositions:
                    if i["side"] == "long":
                        try:
                            self.exchange.create_market_order(i["symbol"], "sell", i["contracts"],self.leverage, params={'leverage': self.leverage})
                        except Exception as e:
                            self.logger.error("Cannot create market order!" + str(e))
                        self.logger.info( f"-------- Close buy position on {i['symbol']}--------")
                    elif i["side"] == "short":
                        try:
                            self.exchange.create_market_order(i["symbol"], "buy", i["contracts"],self.leverage, params={'leverage': self.leverage})
                        except Exception as e:
                            self.logger.error("Cannot create market order!" + str(e))
                        self.logger.info( f"-------- Close sell position on {i['symbol']}--------")
                for index, k in dbPositions.iterrows():
                    self.logger.info(f"-------------- Closing position {k['id']} in database! --------------")
                    self.db.close_position(k["id"])
                    self.db.close_order_by_positionId(k["id"])
                self.openPositions = []