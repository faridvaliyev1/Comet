from Utils.DBContext import DbContext
import re

Aliases=[
    ["T0","T1"],
    ["T_User","T_City"],
    ["T0"],
    ["T0"],
    ["T_User","T_City"],
    ["S0","S1"],
    ["S0"],
    ["S0","S3"],
    ["S0","S3"],
    ["S0"],
    ["S0"],
    ["T0","T1"],
    ["V0","V3"],
    ["V0","V1"],
    ["V0","V5","V4"],
    ["V0","V1","V2","V7"],
    ["V0","V1","V2"],
    ["V0","V4","V7"],
    ["V0","V2","V3","V7","V4","V8"],
    ["T0"],

]

f=open("queries.txt","r")
queries=[]
query=""
for line in f.readlines():
    if line.count("--END--")>0:
        queries.append(query)
        query=""
    else:
        query+=line
    

def find_tables_columns(Tables,sql):
    tables_dict={}
    special_characters=["(",")",","," ","=","\n"]
    keywords=["ON","JOIN","SELECT"]
    for table in Tables:
        columns=["Subject"]
        pattern=table+"\."
        for m in re.finditer(pattern,sql):
            column=""
            for index in range(m.end(),len(sql)):
                if special_characters.count(sql[index])==0:
                    
                    column=column+sql[index]
                else:
                    break
            if column.upper() not in keywords:
                columns.append(column)

            tables_dict[table]=list(set(columns))
    
    return tables_dict

def find_table_info(Tables):
    tables_dict={}
    for table in Tables:
        columns=[]
        data=DbContext.Select(f"""select column_name from global_mapping where table_name='{table}'""")
        for element in data:
            columns.append(element[0])
        
        tables_dict[table]=columns

    return tables_dict
        

def create_join(*columns):

    sql=f"""select distinct table_name
            from global_mapping
            where column_name in {columns}
                                    """
    distinct_tables=DbContext.Select(sql)

    select_columns=''

    for column in columns:
        select_columns+=f'{column},'
    
    select_columns=select_columns[:-1]

    sql=f"""select table_name,c.column_name,count(*) over (partition by table_name) as count_ from global_mapping gm
            join (select count(*) as count_,column_name from global_mapping 
            where column_name in {columns} and column_name<>'Subject'
            group by column_name 
            having count(*)>1) c on gm.column_name =c.column_name
            order by count_ desc"""

    multiple_predicates=DbContext.Select(sql)
    columns_dict={}
    for element in multiple_predicates:
        columns_dict.setdefault(element[1],[]).append(element[0])
    
    
    if(len(multiple_predicates)!=0):
        Tables=[]
        for table in multiple_predicates:
            Tables.append(table[0])
        
        
        tables_dict=find_table_info(Tables)
        # for item in multiple_predicates:
        #     tables_dict.setdefault(item[0],[]).append(item[1])
        
        best_count=0
        best_table=""
        tables=[]
        print(columns_dict)
        for k,v in columns_dict.items():
            for element in v:
                
                if sorted(tables_dict[element])==sorted(list(columns)):

                    distinct_tables=[element]

                    break
                else:
                    intersection_count=len(set(tables_dict[element]).intersection(set(columns)))
                    
                    if best_count<intersection_count:
                        best_count=intersection_count
                        best_table=element
                    elif best_count==intersection_count:
                        
                        sql=f"""select count(*) from {best_table} t1,global_mapping gm
                            where gm.table_name ='{best_table}'"""
                        
                        old_table_size=DbContext.Select(sql)[0]
                        
                        sql=f"""select count(*) from {element} t1,global_mapping gm
                            where gm.table_name ='{element}'"""

                        new_table_size=DbContext.Select(sql)[0]

                        if old_table_size>=new_table_size:
                            best_table=element
            
            tables.append(best_table)
            best_count=0
            best_table=""

        distinct_tables=list(set(tables))        
    else:
        distinct_tables=[table[0] for table in distinct_tables]
        
                
    join=f"""Select {select_columns} from """.replace("(","").replace(")","").replace("'","").replace("Subject",distinct_tables[0]+".Subject")
    
    for index in range(len(distinct_tables)):
        if index==0:
            join+=f" {distinct_tables[index]} "
        else:
            join+=f"""full join {distinct_tables[index]} on {distinct_tables[index]}.Subject={distinct_tables[index-1]}.Subject \n"""
    
    return join

for index in range(len(queries)):
    tables_dict=find_tables_columns(Aliases[index],queries[index])
    print(tables_dict)
    for key,value in tables_dict.items():
        join=create_join(*value)
        queries[index]=queries[index].replace(f"WPT {key}",f"({join}) as {key}")
    
    f=open("queries_h20_100k.txt","a")
    f.write(queries[index]+"\n--END--")
    f.close()