import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
import Configurations


#Database configuration
engine = create_engine(
f"""postgresql://{Configurations.DATABASE_USER}:{Configurations.DATABASE_PASSWORD}@
{Configurations.DATABASE_HOST}:{Configurations.DATABASE_PORT}/{Configurations.DATABASE_NAME}"""
)

conn = psycopg2.connect(
   database=Configurations.DATABASE_NAME, 
   user=Configurations.DATABASE_USER, 
   password=Configurations.DATABASE_PASSWORD, 
   host=Configurations.DATABASE_HOST, 
   port= Configurations.DATABASE_PORT
)
conn.autocommit = True
# End database configuration

class Helper(object):

    @staticmethod
    def Save_Csv_To_Sql(wpt):
        wpt=pd.read_csv("Data/wpt.csv")
        wpt.to_sql("wpt_tbl",engine)
        return wpt

    #Sql level operations
    @staticmethod
    def Select(query):
        pass

    @staticmethod
    def Insert(query):
        pass

    