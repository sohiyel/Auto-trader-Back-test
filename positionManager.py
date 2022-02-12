from position import Position
import uuid

class PositionManager():
    def __init__(self) -> None:
        self.openPositions = []
        self.closedPositions = []
    
    def openPosition(self, pair, type, price, volume, timestamp, stopLoss="", takeProfit="", comment=""):
        positionId = uuid.uuid4()
        newPosition = Position(positionId, pair, type, volume, price, price, timestamp, stopLoss, takeProfit, comment)
        self.openPositions.append(newPosition)

    def closePosition(self, timestamp):
        self.openPositions[0].closePosition(timestamp)