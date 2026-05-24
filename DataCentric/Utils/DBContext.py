import pandas as pd
from pandas.errors import ParserError
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
            try:
                wpt=pd.read_csv(file)
            except ParserError as exc:
                print(f"CSV parse warning: {exc}")
                print("Retrying with malformed rows skipped.")
                wpt=pd.read_csv(file,engine="python",on_bad_lines="skip")
            # wpt.columns=map(str.lower,wpt.columns)
            wpt.to_sql("wpt_tbl",engine,index=False,if_exists="replace")
            print(f"Imported {len(wpt)} rows into wpt_tbl")
        except Exception as exc:
            raise RuntimeError(
                f"Failed to import CSV '{file}' into table 'wpt_tbl': {exc}"
            ) from exc
        
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
