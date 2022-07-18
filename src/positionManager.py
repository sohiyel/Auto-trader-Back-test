from src.position import Position
import uuid
from src.databaseManager import DatabaseManager
from src.utility import Utility
from src.markets import Markets
from src.logManager import LogService
import time
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

    def check_open_position_margin(self, newMargin):
        #Check margin
        dbOpenPositions = self.db.get_open_positions(Utility.get_db_format(self.pair))        
        totalMargin = 0
        for index, k in dbOpenPositions.iterrows():
            if k["side"] == "buy":
                totalMargin += k["volume"] * k["entryPrice"] * self.contractSize
            else:
                if self.settings.isSpot:
                    totalMargin -= k["volume"] * k["entryPrice"] * self.contractSize
                else:
                    totalMargin += k["volume"] * k["entryPrice"] * self.contractSize
        totalMargin = abs(float(totalMargin)) + newMargin
        self.logger.debug(dbOpenPositions)
        self.logger.debug("Total Margin: "+str(totalMargin))
        self.logger.debug("Initial Deposit: "+str(self.initialCapital))
        self.logger.debug("Total Margin / Initial Deposit: "+str(totalMargin / self.initialCapital))
        self.logger.debug("Valid Margin Ratio: "+ str(self.settings.constantNumbers["margin_ratio"]))
        if totalMargin / self.initialCapital > self.settings.constantNumbers["margin_ratio"]:
            self.logger.warning(f"This pair({self.pair}) has reached the maximum ratio of your initial deposit!")
            return False
        return True
        
    def check_open_position_time(self, dbPositions):
        #Check time difference between orders
        if dbPositions.shape[0] > 0:
            if self.botName:
                lastOrderTimestamp = int(dbPositions.loc[dbPositions["botName"] == self.botName].iloc[-1]["openAt"])
            else:
                lastOrderTimestamp = int(dbPositions.loc[dbPositions["strategyName"] == self.strategyName].iloc[-1]["openAt"])
            timeDifference = (time.time() * 1000) - lastOrderTimestamp
            self.logger.debug("Last order time stamp: " + str(lastOrderTimestamp))
            validTimeDifference = Utility.array[self.timeFrame] * 60000 * self.settings.constantNumbers["open_position_delays"]
            self.logger.debug("Current time difference between orders: " + str(timeDifference / 60000))
            self.logger.debug("Valid time difference between orders: " + str(validTimeDifference / 60000))
            if timeDifference < validTimeDifference:
                self.logger.warning(f"Time deference between positions is less that {self.settings.constantNumbers['open_position_delays']} candles!")
                return False

        return True

    
    def open_position(self, signal, lastState):
        positionId = uuid.uuid4().hex
        if self.settings.task == 'trade':
            orderbook = self.exchange.fetch_order_book(self.pair)
            bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
            spread = (ask - bid) if (bid and ask) else None
            self.logger.debug('market price', {'bid': bid, 'ask': ask, 'spread': spread})
            price = bid if signal.side == 'buy' else ask
            dbPositions = self.db.get_positions(Utility.get_db_format(self.pair))
            if self.ratioAmount > 0:
                amount = self.ratioAmount * self.initialCapital / price
                if self.settings.isSpot:
                    if amount > self.contractSize:
                        volume = amount
                    else:
                        volume = self.contractSize
                        self.logger.warning("Volume size is lower than the minimum size!")
                else:
                    volume = amount / self.contractSize
                if self.check_open_position_margin(self.ratioAmount * self.initialCapital) and self.check_open_position_time(dbPositions):
                    pass
                else:
                    self.logger.warning("Cannot open this order!")
                    return
            else:
                if self.settings.isSpot:
                    if self.volume > self.contractSize:
                        volume = self.volume
                    else:
                        volume = self.contractSize
                        self.logger.warning("Volume size is lower than the minimum size!")
                else:
                    volume = self.volume / self.contractSize
                if self.check_open_position_margin(self.volume * price * self.contractSize) and self.check_open_position_time(dbPositions):
                    pass
                else:
                    self.logger.warning("Cannot open this order!")
                    return
            amount = volume
            try:
                if signal.side == 'buy':
                    self.logger.debug(f"Open buy order with volume: {volume}")
                    self.exchange.create_market_order(self.pair,
                                                        signal.side,
                                                        volume,
                                                        self.leverage,
                                                        'open_buy')
                elif signal.side == 'sell':
                    self.logger.debug(f"Open sell order with volume: {volume}")
                    self.exchange.create_market_order(self.pair,
                                                        signal.side,
                                                        volume,
                                                        self.leverage,
                                                        'open_sell')
                stopLossOrderId = uuid.uuid4().hex
                takeProfitOrderId = uuid.uuid4().hex
                try:
                    self.db.add_position(positionId, Utility.get_db_format(signal.pair), signal.side, amount, signal.price, lastState, self.leverage, True, self.timeFrame, self.strategyName, self.botName, stopLossOrderId, takeProfitOrderId)
                    newPosition = Position(positionId, signal.pair, signal.side, self.volume, self.contractSize, signal.price, lastState, self.timeFrame, self.strategyName, self.botName, stopLossOrderId, takeProfitOrderId, True, self.leverage, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment, self.settings)                
                    self.openPositions.append(newPosition)
                    self.logger.info ( f"-------- Open {signal.side} position on {self.openPositions[0].pair}--------")
                    try:
                        self.db.add_order(stopLossOrderId, signal.pair, Utility.opposite_side(signal.side), amount, newPosition.stopLoss, self.leverage, True, self.timeFrame, self.strategyName, self.botName, positionId)
                        self.db.add_order(takeProfitOrderId, signal.pair, Utility.opposite_side(signal.side), amount, newPosition.takeProfit, self.leverage, True, self.timeFrame, self.strategyName, self.botName, positionId)
                    except Exception as e:
                        self.logger.error("Cannot add new order to db!" + str(e))
                except Exception as e:
                    self.logger.error("Cannot add new position to db!" + str(e))
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
        else:
            newPosition = Position(positionId, signal.pair, signal.side, self.volume, self.contractSize, signal.price, lastState, self.timeFrame, self.strategyName, self.botName, '', '', True, self.leverage, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment, self.settings)
            self.openPositions.append(newPosition)
            self.logger.info ( f"-------- Open {signal.side} position on {self.openPositions[0].pair}--------")

    def close_position(self, timestamp):
        if len(self.openPositions) > 0:
            if self.settings.task == 'trade': #self.exchange:
                if self.openPositions[0].side == "buy":
                    try:
                        if self.settings.isSpot:
                            self.exchange.create_market_order(self.exchange.change_symbol_for_trade(self.openPositions[0].pair), "sell", self.openPositions[0].volume)
                        else:
                            self.logger.debug("self.openPositions[0].volume: " + str(self.openPositions[0].volume))
                            self.logger.debug("self.contractSize: " + str(self.contractSize))
                            self.exchange.create_market_order(self.exchange.change_symbol_for_trade(self.openPositions[0].pair), "sell", self.openPositions[0].volume / self.contractSize,self.leverage, 'close_buy')
                        self.logger.info ( f"-------- Close buy position on {self.openPositions[0].pair}--------")
                    except Exception as e:
                        self.logger.error("Cannot create market order!" + str(e))
                elif self.openPositions[0].side == "sell":
                    try:
                        if self.settings.isSpot:
                            self.exchange.create_market_order(self.exchange.change_symbol_for_trade(self.openPositions[0].pair), "buy", self.openPositions[0].volume)
                        else:
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
            self.logger.warning("There is no position to close!")
            return

    def add_volume(self, price, volume):
        self.logger.info("Volume added!")
        return
        self.openPositions[0].entryPrice = (self.openPositions[0].entryPrice * self.openPositions[0].volume + price * volume) / ( self.openPositions[0].volume + volume )
        self.openPositions[0].volume += volume

    def check_sl_tp(self, currentPrice, timestamp):
        for i in self.openPositions:
            self.logger.debug(f"Check sl and tp for {i.pair}")
            self.logger.debug(f"Current price :{currentPrice}")
            self.logger.debug(f"Take profit :{i.takeProfit}")
            self.logger.debug(f"Stop loss :{i.stopLoss}")
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
        self.logger.debug(f"Calculating equities for {len(self.openPositions)} positions...")
        for i in self.openPositions:
            totalEquity += i.calc_equity()
        return totalEquity

    def position_average_price(self):
        return 0

    def position_size(self):
        return 0

    def sync_positions(self):
        dbPositions = self.db.get_open_positions(Utility.get_db_format(self.pair))
        ep = ""
        balance = 0
        if self.settings.isSpot:
            response = self.exchange.fetch_balance(self.pair)
            self.logger.debug(response)
            balance = response['Balance']
            self.logger.debug("balance:"+str(balance))
        else:
            exchangePositions = self.exchange.fetch_positions()
            self.logger.debug(exchangePositions)
            for i in exchangePositions:
                if i.pair == self.exchange.change_symbol_for_trade(self.pair):
                    ep = i
        if ep == "" and balance == 0:
            self.logger.info(f"-------------- There is no position with this pair({self.pair}) in exchange!--------------")
            if len(dbPositions) > 0:
                self.logger.info(f"-------------- There are some extra position with this pair({self.pair}) in database!--------------")
                for index, k in dbPositions.iterrows():
                    self.logger.info(f"-------------- Closing position {k['id']} in database! --------------")
                    self.db.close_position(k["id"])
                    self.db.close_order_by_positionId(k["id"])
                self.openPositions = []
                return True
        else:
            self.logger.info(f"-------------- There is a position with this pair({self.pair}) in exchange!--------------")
            dbVolumes = 0
            pos = None
            for index, k in dbPositions.iterrows():
                if k["timeFrame"] == self.timeFrame and (k["strategyName"] == self.strategyName or k["botName"] == self.botName):
                    self.logger.info(f"-------------- There is a position with this pts in database!--------------")
                    pos = k
                dbVolumes += k["volume"]
            if self.settings.isSpot:
                if float(dbVolumes) == balance:
                    self.logger.info(f"-------------- Positions in exchange match the positions in database! --------------")
                    if pos is None:
                        self.logger.warning(f"-------------- Cannot find database position! --------------")
                    else:
                        self.logger.info(f"-------------- Adding database position to ram! --------------")
                        positionId = uuid.uuid4().hex
                        try:
                            self.openPositions.append(Position(positionId, pos["pair"], pos["side"], float(pos["volume"]), self.contractSize, float(pos["entryPrice"]),
                                                                pos["openAt"], self.timeFrame, self.strategyName, self.botName, pos["stopLossOrderId"],
                                                                pos["takeProfitOrderId"], True, int(pos["leverage"]),settings=self.settings))
                            return True
                        except Exception as e:
                            self.logger.error("Cannot add position to openPositions:"+ str(e))
                            return False
            else:
                self.logger.debug("dbVolume:"+str(dbVolumes))
                self.logger.debug("eVolume:"+str(ep.volume))
                if float(dbVolumes) == float(ep.volume):
                    self.logger.debug("Volumes are matched!")
                    if int(self.leverage) == int(ep.leverage):
                        self.logger.debug("Leverages are matched!")
                        if pos is not None:
                            self.logger.info(f"-------------- Positions in exchange match the positions in database! --------------")
                            try:
                                side = pos["side"]
                                if pos["side"] == "long":
                                    side = "buy"
                                elif pos["side"] == "short":
                                    side = "sell"
                                positionId = uuid.uuid4().hex
                                self.logger.debug('pos["volume"]: '+ str(pos["volume"]))
                                self.openPositions.append(Position(positionId, pos["pair"], side, float(pos["volume"]), self.contractSize, float(pos["entryPrice"]),
                                                                    float(pos["openAt"]), self.timeFrame, self.strategyName, self.botName, pos["stopLossOrderId"],
                                                                    pos["takeProfitOrderId"], True, int(pos["leverage"]),settings=self.settings))
                                return True
                            except Exception as e:
                                self.logger.error("Cannot add position to openPositions:"+ str(e))
                                return False
            
            self.logger.warning(f"-------------- Positions in exchange does not match the positions in database! --------------")
            if self.settings.isSpot:
                try:
                    self.logger.info(f"-------------- Closing position in exchange! --------------")
                    self.exchange.create_market_order(self.pair, "sell", balance)
                except Exception as e:
                    self.logger.error("Cannot create market order!" + str(e))
                    return False
            else:
                try:
                    self.exchange.close_positions(self.pair)
                except Exception as e:
                    self.logger.error("Cannot close position!" + str(e))
                    return False
            try:
                for index, k in dbPositions.iterrows():
                    self.logger.info(f"-------------- Closing position {k['id']} in database! --------------")
                    self.db.close_position(k["id"])
                    self.db.close_order_by_positionId(k["id"])
                self.openPositions = []
                return True
            except Exception as e:
                self.logger.error("Cannot close positions in db!" + str(e))
                return False
        return False