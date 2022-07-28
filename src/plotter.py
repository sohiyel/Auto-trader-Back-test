import pandas as pd
import os
import datetime

class Plotter():
    def __init__(self, filename, settings) -> None:
        self.settings = settings
        self.fileName = str(datetime.datetime.utcfromtimestamp(datetime.datetime.timestamp(datetime.datetime.now())).strftime('%Y%m%d_%H%M%S'))+ "_" + filename

    def writeDFtoFile(self,df):
        pd.DataFrame.to_csv(df,os.path.join(self.settings.REPORTS_DIR,self.fileName))