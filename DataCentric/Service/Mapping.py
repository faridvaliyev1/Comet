from tkinter import W
from Utils.DBContext import DbContext,conn

class Mapping:
    def __init__(self,Tables):

        self.Tables=Tables

        self.initialize()
        
    #----------private functions--------------

    def initialize(self):
        for index in range(len(self.Tables)):
            if len(self.Tables[index])>0:
                self.createMapping(self.Tables[index],"tables_"+str(index))
    
    def partition_wpt(self,Cluster):
        pass

    def DropColumn(self,Columns,table_name):
        for column in Columns.split(','):
            sql=f"""
            ALTER TABLE {table_name} drop column {column};
                """
            DbContext.Insert(sql,None)
         
    def find_columns_information(self,Cluster):
        sql="""SELECT COLUMN_NAME,TYPE_NAME FROM METRICS WHERE COLUMN_NAME IN (columns)"""
        columns=""
        for item in Cluster:
            columns+="'" +item +"'"+","
        
        columns=columns[0:len(columns)-1]
        sql=sql.replace("columns",columns)

        data=DbContext.Select(sql)

        return data
    
    def Create_Table(self,Table,Columns):
        sql=f"""
        DROP TABLE IF EXISTS {Table};
        CREATE TABLE {Table}(
        Subject VarChar,
        columns
        )
        """
        elements=""
        for element in Columns:
            elements+=f""""{element[0]}" {element[1]},"""

        elements=elements[0:len(elements)-1]

        sql=sql.replace("columns",elements)
        DbContext.Insert(sql,None)
    
    def fill_data(self,Table,Columns):
        sql=f"""
        INSERT INTO {Table}
        SELECT DISTINCT Subject,{Columns} from wpt_tbl
        WHERE
        """
        for column in Columns.split(','):
            sql+=column+" IS NOT NULL OR "
        
        sql=sql[0:len(sql)-4]
        DbContext.Insert(sql,None)
    
    def create_global_mapping(self,Table,Columns):
        sql="""
            CREATE TABLE IF NOT EXISTS 
            GLOBAL_MAPPING(
                COLUMN_NAME text,
                TABLE_NAME text
            );
        """
        
        DbContext.Insert(sql,None)

        for column in Columns:
            DbContext.Insert("INSERT INTO GLOBAL_MAPPING (COLUMN_NAME,TABLE_NAME) VALUES (%s,%s)",[(column[0],Table)])
        

    
    def createMapping(self,Cluster,Table_Name):
        
        columns=self.find_columns_information(Cluster)
        self.Create_Table(Table_Name,columns)

        cols=""
        for column in columns:
            cols+=f""""{column[0]}","""
        
        cols=cols[0:len(cols)-1]

        self.fill_data(Table_Name,cols)
        

        self.create_global_mapping(Table_Name,columns)
        
        
        #self.DropColumn(cols,"wpt_tbl")
        
        sql="""
        SELECT column_name,data_type FROM information_schema.columns
        where table_name='wpt_tbl' and table_schema='public'
        """
        columns=DbContext.Select(sql)
        
        # self.CalculateMetrics(columns)
    #---------end of private functions--------

    def copy_to_table(self):
        
        sql="SELECT distinct TABLE_NAME FROM GLOBAL_MAPPING"

        tables=DbContext.Select(sql)

        for table in tables:

            sql=f"COPY (SELECT * FROM {table[0]}) TO STDOUT WITH CSV HEADER"

            cursor=conn.cursor()

            with open("Data/results2/h20_100M/"+f"{table[0]}.csv", "w") as file:
                cursor.copy_expert(sql, file)