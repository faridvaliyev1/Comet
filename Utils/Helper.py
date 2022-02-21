import pandas as pd

class Helper(object):

    @staticmethod
    def Read_csv(csv):
        pd.read_csv(csv)
        return pd