from position import Position
import uuid

class PositionManager():
    def __init__(self, exchange="") -> None:
        self.openPositions = []
        self.closedPositions = []
        self.exchange = exchange
    
    def open_position(self, signal, lastState):
        if self.exchange:
            self.exchange.create_market_order(signal.pair, signal.type, signal.volume)
            print ( f"-------- Open {signal.type} position on {self.openPositions[0].pair}--------")
        positionId = uuid.uuid4()
        newPosition = Position(positionId, signal.pair, signal.type, signal.volume, signal.price, lastState, signal.stopLoss, signal.takeProfit, signal.slPercent, signal.tpPercent, signal.comment)
        self.openPositions.append(newPosition)

    def close_position(self, timestamp):
        if len(self.openPositions) > 0:
            if self.exchange:
                if self.openPositions[0].type == "buy":
                    self.exchange.create_market_order(self.openPositions[0].pair, "sell", self.openPositions[0].volume)
                    print ( f"-------- Close buy position on {self.openPositions[0].pair}--------")
                elif self.openPositions[0].type == "sell":
                    self.exchange.create_market_order(self.openPositions[0].pair, "buy", self.openPositions[0].volume)
                    print ( f"-------- close sell position on {self.openPositions[0].pair}--------")
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
            i.profit = i.calcProfit()
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
            totalEquity += i.calcEquity()
        return totalEquity

    def position_average_price(self):
        return 0

    def position_size(self):
        return 0