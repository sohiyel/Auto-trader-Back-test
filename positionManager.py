from position import Position
import uuid

class PositionManager():
    def __init__(self) -> None:
        self.openPositions = []
        self.closedPositions = []
    
    def openPosition(self, signal, lastState):
        positionId = uuid.uuid4()
        newPosition = Position(positionId, signal.pair, signal.type, signal.volume, signal.price, lastState, signal.stopLoss, signal.takeProfit, signal.comment)
        self.openPositions.append(newPosition)

    def closePosition(self, timestamp):
        if len(self.openPositions) > 0:
            lastPrice = self.openPositions[0].closePosition(timestamp)
            self.closedPositions.append(self.openPositions[0])
            self.closedPositions[-1].calcProfit()
            self.openPositions = []
            return lastPrice
        else:
            return

    def addVolume(self, price, volume):
        self.openPositions[0].openPrice = (self.openPositions[0].openPrice * self.openPositions[0].volume + price * volume) / ( self.openPositions[0].volume + volume )
        self.openPositions[0].volume += volume

    def updatePositions(self, currentPrice, timestamp):
        for i in self.openPositions:
            i.currentPrice = currentPrice
            i.profit = i.calcProfit()
            if i.type == 'LONG':
                if i.takeProfit > 0:
                    if currentPrice > i.takeProfit:
                        self.closePosition(timestamp)
                if i.stopLoss > 0:
                    if currentPrice < i.stopLoss:
                        self.closePosition(timestamp)
            elif i.type == 'SHORT':
                if i.takeProfit > 0:
                    if currentPrice < i.takeProfit:
                        self.closePosition(timestamp)
                if i.stopLoss > 0:
                    if currentPrice > i.stopLoss:
                        self.closePosition(timestamp)

    def calcEquity(self):
        totalEquity = 0
        for i in self.openPositions:
            totalEquity += i.calcEquity()
        return totalEquity

    def positionAveragePrice(self):
        return 0

    def positionSize(self):
        return 0