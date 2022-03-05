from warnings import catch_warnings
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
import Configurations

#Database configuration
engine = create_engine(Configurations.DATABASE_ENGINE)

conn = psycopg2.connect(**Configurations.CONNECTION_CONFIG_DICT)
conn.autocommit = True
# End database configuration

class Helper(object):


    @staticmethod
    def Save_Csv_To_Sql(wpt):
        try:
            wpt=pd.read_csv("Data/wpt.csv")
            wpt.to_sql("wpt_tbl",engine)
        except:
            print("Operation is failed..")
        
    #Sql level operations
    @staticmethod
    def Select(query):
        pass

    @staticmethod
    def Insert(query):
        pass

    