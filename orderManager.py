from order import Order
import uuid

class OrderManagert():
    def __init__(self) -> None:
        self.openOrders = []
        self.closedOrders = []
    
    def openOrder(self, pair, type, price, volume, timestamp, stopLoss="", target=""):
        orderId = uuid.uuid4()
        newOrder = Order(orderId, pair, type, volume, price, price, timestamp)
        self.openOrders.append(newOrder)

    def closeOrder(self, timestamp):
        self.openOrders[0].closeOrder(timestamp)