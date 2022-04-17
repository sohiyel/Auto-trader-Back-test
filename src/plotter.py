import pandas as pd
import os
import datetime
from account.settings.settings import Settings

class Plotter():
    def __init__(self, filename) -> None:
        self.fileName = str(datetime.datetime.timestamp(datetime.datetime.now()))+ "_" + filename

    def writeDFtoFile(self,df):
        pd.DataFrame.to_csv(df,os.path.join(Settings.REPORTS_DIR,self.fileName))