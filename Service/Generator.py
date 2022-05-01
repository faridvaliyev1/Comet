import re

from sqlalchemy import distinct
from Utils.DBContext import DbContext

class Generator:
    def __init__(self):
        pass

    #--- private functions-----
    def find_columns(self,query):
        return re.findall(r'(?:(?i)WHERE|SELECT|AND|OR|GROUP BY|ORDER BY|THEN|ELSE|CASE WHEN|ON|=) \(?([a-zA-Z0-9.,]+)', query)
    
    def find_tables(self,query):
        return re.findall(r'(?:(?i)FROM|JOIN|=) \(?([a-zA-Z0-9.,]+)', query)
    
    def find_migrations(self,query):

        mappings=DbContext.Select("SELECT * FROM GLOBAL_MAPPING")
        column_dict={}
        columns=self.find_columns(query)
        for column in columns:
            column_part=""
            schema_part=""
            if "." in column:
                schema_part=column.split(".")[0]
                column_part=column.split(".")[1]

            for mapping in mappings:
                if column_part in mapping[0]:
                    column_dict[column_part]=(schema_part,mapping[1])
        
        return column_dict
    
    def construct_join_statement(self,tables):

        joins=""
        for index in range(len(list(tables))):
            if index==0:
                joins=f"FROM {tables[index]} "
            else:
                joins+=f"""LEFT OUTER JOIN {tables[index]} 
                                             ON {tables[index]}.Subject={tables[index-1]}.Subject"""
        
        return joins
                        
    def construct_query(self,query):

        tables_dict=self.find_migrations(query)
        old_tables=self.find_tables(query)
        distinct_tables=list(set(value[1] for value in tables_dict.values()))
        
        for key,value in tables_dict.items():
            query=query.replace(value[0]+"."+key,value[1]+"."+key)
        
        return query