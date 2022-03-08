import imp
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
import Configurations
from Formulas import Formulas

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
        try:
            cursor=conn.cursor()

            cursor.execute(query=query)

            data=cursor.fetchall()

            return data
        except:

            raise ValueError("Operation is failed")

        finally:
            cursor.close()
            conn.close()
        
    @staticmethod
    def Insert(query,params):
        try:
            cursor=conn.cursor()

            cursor.executemany(query,params)
        except:
            raise ValueError("Operation is failed")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def Create_Mapping(query):

        sql="""
            DROP TABLE GLOBAL_MAPPING;
            CREATE TABLE GLOBAL_MAPPING(
            ID SERIAL,
            COLUMN_NAME VARCHAR(50),
            TABLE_NAME VARCHAR(100)
            );
            """
        
        cursor=conn.cursor()

        cursor.execute(sql)

    @staticmethod
    def CreateSchema(schema_name):
        sql=f"""DROP SCHEMA {schema_name};CREATE SCHEMA {schema_name}"""

        cursor=conn.cursor()

        cursor.execute(sql)

        return schema_name
    
    def calculateMetrics(columns):
    
        sql="""SELECT """

        for column in columns:
            sql+=f""" SUM(case when "{str(column[0])}" IS NULL Then 1 else 0 end) as {str(column[0])}_null_count,"""
        
        sql=sql[:-1]
        sql+=" from wpt_tbl"

        cursor=conn.cursor()

        cursor.execute(sql)
        
        
        data=cursor.fetchall()[0]
        tuples=[]
        for x in range(len(columns)):
            new_tuple=(str(columns[x][0]),int(data[x]),
            str(columns[x][1]),
            str(Formulas.metric_total_null(int(str(data[x])),len(columns),22390)),
            str(Formulas.metric_total_null_column(int(str(data[x])),len(columns))),
            str(Formulas.metric_total_null_row(int(str(data[x])),22390)))
            print(f"{x} step tuple {new_tuple}")
            tuples.append(new_tuple)
            new_tuple=()
        
        sql="""DELETE FROM METRICS"""

        cursor.execute(sql)
        
        cursor.executemany("INSERT INTO METRICS (COLUMN_NAME,NULL_COUNT,TYPE_NAME,METRIC_1,METRIC_2,METRIC_3) VALUES (%s,%s,%s,%s,%s,%s)",tuples)

    @staticmethod
    def DropColumn(column_name,table_name):
        sql=f"""
        ALTER TABLE {table_name} drop column "{column_name}";
            """

        cursor=conn.cursor()

        cursor.execute(sql)

    @staticmethod
    def createMapping(column_name,table_name,type_name):
        sql=f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name}(
        ID BIGINT,
        "{column_name}" {type_name}
        )
        """

        cursor=conn.cursor()

        cursor.execute(sql)
        
        sql=f"""
        INSERT INTO {table_name}
        SELECT Index,"{column_name}" from wpt_tbl
        """
        cursor.execute(sql)
        
        cursor.execute("INSERT INTO GLOBAL_MAPPING (COLUMN_NAME,TABLE_NAME) VALUES (%s,%s)",(column_name,table_name))
        
        DropColumn(column_name,"wpt_tbl")
        
        sql="""
        SELECT column_name,data_type FROM information_schema.columns
        where table_name='wpt_tbl' and table_schema='public'
        """
        
        cursor.execute(sql)

        columns=cursor.fetchall()
        
        calculateMetrics(columns)
    
    
        
        
        