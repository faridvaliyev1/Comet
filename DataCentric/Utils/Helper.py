from Utils.Formulas import Formulas
from Utils.DBContext import DbContext

class Helper:

    def Create_Mapping(query):

        sql="""
            DROP TABLE GLOBAL_MAPPING;
            CREATE TABLE GLOBAL_MAPPING(
            ID SERIAL,
            COLUMN_NAME VARCHAR(50),
            TABLE_NAME VARCHAR(100)
            );
            """
        DbContext.Insert(sql)

    def CreateSchema(schema_name):
        pass

    def CalculateMetrics(columns):
        
        sql="SELECT COUNT(*) as count from wpt_tbl"
        
        total_count=DbContext.Select(sql)[0][0]
        sql="""SELECT """

        for column in columns:
            sql+=f"""SUM(case when "{str(column[0])}" IS NOT NULL Then 1 else 0 end) as {str(column[0])}_not_null_count,"""
        
        sql=sql[:-1]
        sql+=" from wpt_tbl"
        data=DbContext.Select(sql)[0]

        tuples=[]
        for x in range(len(columns)):
            new_tuple=(str(columns[x][0]),int(data[x]),
            str(columns[x][1]),
            str(Formulas.metric_total_null(int(str(data[x])),len(columns),total_count)),
            str(Formulas.metric_total_null_column(int(str(data[x])),len(columns))),
            str(Formulas.metric_total_null_row(int(str(data[x])),total_count)))
            tuples.append(new_tuple)
            new_tuple=()
        
        # If tables doesnt exist then create
        sql=f"""CREATE TABLE IF NOT EXISTS Metrics(
            COLUMN_NAME VARCHAR(500),
            NOT_NULL_COUNT INTEGER,
            TYPE_NAME  VARCHAR(50),
            METRIC_1  DECIMAL(18,2),
            METRIC_2  DECIMAL(18,2),
            METRIC_3  DECIMAL(18,3)
        );
        """
        DbContext.Insert(sql,None)

        sql="""DELETE FROM METRICS"""
        
        DbContext.Insert(sql,None)
        
        query="INSERT INTO METRICS (COLUMN_NAME,Not_Null_Count,TYPE_NAME,METRIC_1,METRIC_2,METRIC_3) VALUES (%s,%s,%s,%s,%s,%s)"

        DbContext.Insert(query,tuples)

    def GetColumnInformation():
        sql="""
        SELECT column_name,data_type FROM information_schema.columns
        where table_name='wpt_tbl' and table_schema='public'
        """
        data=DbContext.Select(sql)
        return data
    
    def SubjectPropertyBasket(columns):
        sql=f"""SELECT "Subject","""

        for column in columns:
            if column[0].lower()!="Subject".lower():
                sql+=f""" CASE WHEN "{str(column[0])}" IS NOT NULL THEN '{column[0]}' ELSE '' END, """
        
        sql=sql[0:len(sql)-2]
        
        sql+=""" FROM WPT_TBL"""

        Baskets=DbContext.Select(sql)
        SubjectPropertyBaskets={}

        for basket in Baskets:
            elements=[]
            for index in range(1,len(basket)):

                if basket[index]!="":
                    elements.append(basket[index])
            
            SubjectPropertyBaskets[basket[0]]=elements
        
        return SubjectPropertyBaskets


    
        
        
        