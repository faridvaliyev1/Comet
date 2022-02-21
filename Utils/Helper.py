import pandas as pd

class Helper(object):

    #Simple File operations
    @staticmethod
    def Read_csv(csv):
        pd.read_csv(csv)
        return pd
    
    @staticmethod
    def Save_Csv_To_Sql(csv):
        pass

    #Sql level operations
    @staticmethod
    def Select(query):
        pass

    @staticmethod
    def Insert(query):
        pass

    