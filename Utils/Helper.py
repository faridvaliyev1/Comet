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
        sql=f"""DROP SCHEMA {schema_name};CREATE SCHEMA {schema_name}"""

        DbContext.Insert(sql)
        
        return schema_name
    

    def CalculateMetrics(columns):
        
        sql="SELECT COUNT(*) as count from wpt_tbl"
        
        total_count=DbContext.Select(sql)[0]
        print(total_count)
        sql="""SELECT """

        for column in columns:
            sql+=f""" SUM(case when "{str(column[0])}" IS NOT NULL Then 1 else 0 end) as {str(column[0])}_not_null_count,"""
        
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
            print(f"{x} step tuple {new_tuple}")
            tuples.append(new_tuple)
            new_tuple=()
        
        sql="""DELETE FROM METRICS"""

        DbContext.Insert(sql,())

        query="INSERT INTO METRICS (COLUMN_NAME,Not_Null_Count,TYPE_NAME,METRIC_1,METRIC_2,METRIC_3) VALUES (%s,%s,%s,%s,%s,%s)"
        DbContext.Insert(query,tuples)

    def GetColumnInformation():
        sql="""
        SELECT column_name,data_type FROM information_schema.columns
        where table_name='wpt_tbl' and table_schema='public'
        """
        data=DbContext.Select(sql)
        return data

    def DropColumn(column_name,table_name):
        sql=f"""
        ALTER TABLE {table_name} drop column "{column_name}";
            """
        
        DbContext.Insert(sql)

    def createMapping(column_name,table_name,type_name):
        sql=f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name}(
        ID BIGINT,
        "{column_name}" {type_name}
        )
        """

        DbContext.Insert(sql)
        
        sql=f"""
        INSERT INTO {table_name}
        SELECT Index,"{column_name}" from wpt_tbl
        """
        DbContext.Insert(sql)
        
        DbContext.Insert("INSERT INTO GLOBAL_MAPPING (COLUMN_NAME,TABLE_NAME) VALUES (%s,%s)",(column_name,table_name))
         
        DropColumn(column_name,"wpt_tbl")
        
        sql="""
        SELECT column_name,data_type FROM information_schema.columns
        where table_name='wpt_tbl' and table_schema='public'
        """
        columns=DbContext.Select(sql)
        
        CalculateMetrics(columns)
    
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


    
        
        
        