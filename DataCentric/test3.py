from Utils.DBContext import DbContext,conn
def copy_to_table():
        
        sql=f"COPY (select * from wpt_tbl limit 100000) TO STDOUT WITH CSV HEADER"

        cursor=conn.cursor()

        with open(f"Data/results2/wpt_100K.csv", "w") as file:
            cursor.copy_expert(sql, file)


copy_to_table()