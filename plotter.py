import pandas as pd
import os

class Plotter():
    def __init__(self, filename) -> None:
        self.fileName = filename

    def writeDFtoFile(self,df):
        pd.DataFrame.to_csv(df,os.path.join(os.path.curdir,"reports",self.fileName))