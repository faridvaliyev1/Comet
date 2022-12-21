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

class DbContext:

    def __init__(self):
        cursor=conn.cursor()

    def Save_Csv_To_Sql(file):
        try:
            wpt=pd.read_csv(file)
            # wpt.columns=map(str.lower,wpt.columns)
            wpt.to_sql("wpt_tbl",engine,index=False)
        except:
            print("Operation failed")
        
    def Select(query):
        # try:
        cursor=conn.cursor()

        cursor.execute(query=query)

        data=cursor.fetchall()

        return data
        # except:
        #     raise ValueError("Operation is failed")
    
    def Insert(query,params):

        cursor=conn.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.executemany(query,params)