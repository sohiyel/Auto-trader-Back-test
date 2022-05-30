from datetime import datetime
from pytz import timezone
from src.utility import Utility
from src.databaseManager import DatabaseManager
from src.logManager import LogService
class DataService():

    def __init__(self, market, pair, timeFrame, startTime, endTime, historyNeeded = 0, settings=''):
        self.pair = pair
        self.settings = settings
        self.dbPair = Utility.get_db_format(self.pair)
        self.timeFrame = Utility.unify_timeframe(timeFrame, settings.exchange)
        self.tableName = self.dbPair + "_" + self.timeFrame
        self.startTime = startTime
        self.endTime = endTime
        self.dataFrame = ""
        self.market = market
        self.startAtTs = self.convert_time(startTime)
        self.endAtTs = self.convert_time(endTime)
        self.historyNeeded = int(historyNeeded)
        self.db = DatabaseManager(settings, pair, timeFrame)
        self.logService = LogService(__name__, settings)
        self.logger = self.logService.logger  #get_logger(__name__, settings)
        pts = {'pair': self.pair, 'timeFrame': self.timeFrame, 'strategyName': 'NaN'}
        self.logService.set_pts_formatter(pts)
        if not settings.task == 'trade':
            self.fetch_klines()

    @staticmethod
    def convert_time(ttime):
        date_time_obj = datetime.strptime(ttime, '%Y-%m-%d_%H:%M:%S')
        utc_time = date_time_obj.replace(tzinfo=timezone('utc'))
        return int(datetime.timestamp(utc_time))

    def fetch_klines(self):
        try:
            self.logger.info("Fetching klines...")
            self.dataFrame = self.db.fetch_klines(self.pair, self.timeFrame, (self.startAtTs - self.historyNeeded) * 1000, self.endAtTs * 1000)
            self.logger.info("Expected candles:", (self.endAtTs - (self.startAtTs - self.historyNeeded))/(Utility.array[self.timeFrame]*60)[0])
            self.logger.info("Existing candles:", self.dataFrame.shape[0][0])
            self.logger.info("Needed start and end time:", (self.startAtTs - self.historyNeeded)*1000, self.endAtTs*1000)
            self.logger.info("Existed start anad end time:", self.dataFrame.iloc[-1]['timestamp'], self.dataFrame.iloc[0]['timestamp'])
        except:
            self.logger.error("Cannot fetch klines")

    def read_data_from_db(self, limit, lastState):
        return self.db.read_klines(self.dbPair, self.timeFrame, limit, lastState)

    def read_data_from_memory(self, limit, lastState):
        try:
            df = self.dataFrame.loc[self.dataFrame['timestamp'] <= lastState]
            df = df.sort_values(by='timestamp', ascending=True)
            df.reset_index(drop=True, inplace=True)
            return df.tail(limit)
        except:
            self.logger.error("Cannot read klines from memory!")
