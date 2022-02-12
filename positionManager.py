from position import Position
import uuid

class PositionManager():
    def __init__(self) -> None:
        self.openPositions = []
        self.closedPositions = []
    
    def openPosition(self, pair, type, price, volume, timestamp, stopLoss="", takeProfit="", comment=""):
        if len(self.openPositions) < 1:
            positionId = uuid.uuid4()
            newPosition = Position(positionId, pair, type, volume, price, timestamp, stopLoss, takeProfit, comment)
            self.openPositions.append(newPosition)
            return True
        else:
            return False

    def closePosition(self, timestamp):
        if len(self.openPositions) > 0:
            lastPrice = self.openPositions[0].closePosition(timestamp)
            self.closedPositions.append(self.openPositions[0])
            self.openPositions = []
            return lastPrice
        else:
            return 0

    def updatePositions(self, currentPrice):
        for i in self.openPositions:
            i.currentPrice = currentPrice

    def positionAveragePrice(self):
        return 0

    def positionSize(self):
        return 0