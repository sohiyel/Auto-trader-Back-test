from position import Position
import uuid

class PositionManager():
    def __init__(self) -> None:
        self.openPositions = []
        self.closedPositions = []
    
    def openPosition(self, pair, type, price, volume, timestamp, stopLoss="", takeProfit="", comment=""):
        positionId = uuid.uuid4()
        newPosition = Position(positionId, pair, type, volume, price, timestamp, stopLoss, takeProfit, comment)
        self.openPositions.append(newPosition)

    def closePosition(self, timestamp):
        if len(self.openPositions) > 0:
            lastPrice = self.openPositions[0].closePosition(timestamp)
            self.closedPositions.append(self.openPositions[0])
            self.openPositions = []
            return lastPrice
        else:
            return

    def addVolume(self, price, volume):
        self.openPositions[0].openPrice = (self.openPositions[0].openPrice * self.openPositions[0].volume + price * volume) / ( self.openPositions[0].volume + volume )
        self.openPositions[0].volume += volume

    def updatePositions(self, currentPrice):
        for i in self.openPositions:
            i.currentPrice = currentPrice
            i.calcProfit()

    def positionAveragePrice(self):
        return 0

    def positionSize(self):
        return 0