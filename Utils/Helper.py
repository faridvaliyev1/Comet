import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
import settings


#Database configuration
engine = create_engine(
f"""postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@
{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"""
)

conn = psycopg2.connect(
   database=settings.DATABASE_NAME, 
   user=settings.DATABASE_USER, 
   password=settings.DATABASE_PASSWORD, 
   host=settings.DATABASE_HOST, 
   port= settings.DATABASE_PORT
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

    