import pandas as pd
import os
import datetime

class Plotter():
    def __init__(self, filename) -> None:
        self.fileName = str(datetime.datetime.timestamp(datetime.datetime.now()))+ "_" + filename

    def writeDFtoFile(self,df):
        pd.DataFrame.to_csv(df,os.path.join(os.path.curdir,"reports",self.fileName))