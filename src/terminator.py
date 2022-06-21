from src.logManager import LogService
import time

class Terminator():
    def __init__(self, settings) -> None:
        self.settings = settings
        self.logService = LogService(__name__+"|"+settings.exchange, settings)
        self.logger = self.logService.logger
        self.exchange = settings.exchange_service
        self.exchange.authorize()

    def close_spot_positions(self):
        self.logger.debug("Close spot positions:")
        wallet = self.exchange.fetch_accounts()
        if wallet:
            for symbol in wallet:
                if float(wallet[symbol]) > 0:
                    done = True
                    while(done):
                        try:
                            pair = self.exchange.change_symbol_for_trade(symbol+"-"+self.settings.baseCurrency)
                            self.logger.info(f"-------------- Selling {symbol} in {self.settings.exchange}! --------------")
                            self.exchange.create_market_order(pair, "sell", wallet[symbol])
                            time.sleep(1)
                            done = False
                        except Exception as e:
                            self.logger.error("Cannot create market order!" + str(e))
                            time.sleep(10)
        else:
            self.logger.error("Cannot fetch accounts")

    def close_future_positions(self):
        self.logger.debug("Close future positions:")
        try:
            self.exchange.close_positions()
            return
        except Exception as e:
            self.logger.error("Cannot close exchange positions!")

    def close_all_positions(self):
        if self.settings.isSpot:
            self.close_spot_positions()
        else:
            self.close_future_positions()