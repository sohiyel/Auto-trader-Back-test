import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from src.settings import Settings


class LogService():
    def __init__(self, logger_name, settings) -> None:
        self.FORMATTER = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] : %(message)s")
        self.settings = settings
        self.logger = logging.getLogger(logger_name)
        if len(self.logger.handlers) == 0:
            self.logger.setLevel(logging.DEBUG) # better to have too much log than not enough
            self.logger.addHandler(self.get_console_handler())
            self.logger.addHandler(self.get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        self.logger.propagate = False

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.FORMATTER)
        return console_handler

    def get_file_handler(self):
        LOG_FILE = self.settings.LOG_FILE
        file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
        file_handler.setFormatter(self.FORMATTER)
        return file_handler
        
    def set_pts_formatter(self, pts):
        self.filter = PtsFilter()
        self.filter.update_information(pts)
        self.logger.addFilter(self.filter)
        self.FORMATTER = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] / [%(pair)s - %(timeFrame)s - %(strategyName)s] : %(message)s")
        #self.logger.LoggerAdapter(self.logger, {'pair': self.pair, 'timefriame': self.timeframe, 'strategy': self.strategy})
        for handler in self.logger.handlers:
            handler.setFormatter(self.FORMATTER)


class PtsFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def update_information(self, pts):
        self.pair = pts['pair']
        self.timeFrame = pts['timeFrame']
        self.strategyName = pts['strategyName']


    def filter(self, record):

        record.pair = self.pair
        record.timeFrame = self.timeFrame
        record.strategyName = self.strategyName
        return True



