from pickle import TRUE
from re import I
from psycopg2 import connect
from Utils.Helper import Helper 
from Utils.DataStructures import DataStructures
from Utils.DBContext import DbContext

from Service.Clustering import Clustering
from Service.Mapping import Mapping
from Service.Partitioning import Partitioning
from Service.Generator import Generator
from Service.StarPattern import StarPattern
from Configurations import NULL_THRESHOLD

print("---Application is starting------")

print("---CSV is importing--------")

DbContext.Save_Csv_To_Sql("Data/combined_100K.csv")

print("---End of importing------")

print("----Metrics calculation------------")

columns=Helper.GetColumnInformation()
Helper.CalculateMetrics(columns)

print("----End of metrics calculation------------")
print("Data Structure generation")

print("end of data structure generation")

print("Clustering starting...")

support_thresholds=[0.5]
PropertyUsageList=[]
null_thresholds=[15]
Tables=[]
for support_threshold in support_thresholds:

    DS=DataStructures(support_threshold)

    for null_threshold in null_thresholds:

        CS=Clustering(DS.SubjectPropertyBasket,DS.Subject_PropertyBasketCount,DS.PropertyUsageList,DS.Fpgrowth_list,support_threshold,null_threshold)

        PT=Partitioning(CS.Clusters,CS.Tables,DS.PropertyUsageList,null_threshold)

        tables_count=0
        for part in PT.Tables:
         if part is not None:
             tables_count+=1

        Tables.append((support_threshold,null_threshold,PT.Tables))

        PropertyUsageList=DS.PropertyUsageList

        print("-----------------------------------")
        print(f"Support_Threshold: {support_threshold} \n Null_Threshold: {null_threshold} \n Number of tables: {tables_count} ")
        print("------------------------------------")  

# MP=Mapping(PT.Tables)
# MP.copy_to_table()

starPattern=StarPattern("Data/workload.txt")

connectors=starPattern.find_stars()[1]

star_tables=starPattern.combine_stars()

stars=[]
for key,value in star_tables.items():
    if len(value)>0:
        stars.append(tuple(value))


for index in range(len(stars)):
    print(index,":",stars[index])
    print("--------------------")

# for connector in connectors:
#     PT.Tables.append((connector))

# Stars
for tables in PT.Tables:
    if len(tables)!=1:
        for table in tables:
            for star in stars:                
                if table in star and (PropertyUsageList[table]/PropertyUsageList["Subject"])>NULL_THRESHOLD:
                    new_tables=tuple(t for t in tables if t!=table)
# connectors
for tables in PT.Tables:
    if len(tables)!=1:
        for table in tables:
            for connector in connectors:
                    if connector in table and (PropertyUsageList[table]/PropertyUsageList["Subject"])>NULL_THRESHOLD:
                        table=tuple(t for t in tables if t!=table)
        print("-------------------------------------")
# end of connectors

# adding stars to final table
for star in stars:
    PT.Tables.append(star)

MP=Mapping(PT.Tables)
MP.copy_to_table()