from pickle import NONE
import Configurations

from Utils.Helper import Helper 
from Utils.DataStructures import DataStructures
from Utils.DBContext import DbContext

from Service.Clustering import Clustering
from Service.Mapping import Mapping
from Service.Partitioning import Partitioning
from Service.Generator import Generator



print("---Application is starting------")

print("---CSV is importing--------")

DbContext.Save_Csv_To_Sql("Data/combined_csv.csv")

print("---End of importing------")

print("----Metrics calculation------------")

columns=Helper.GetColumnInformation()
Helper.CalculateMetrics(columns)

print("----End of metrics calculation------------")
print("Data Structure generation")



print("end of data structure generation")

print("Clustering starting...")

support_thresholds=[0.1,0.2,0.3,0.4,0.5]
null_thresholds=[5,10,15,20,25,30]
for support_threshold in support_thresholds:

    DS=DataStructures(support_threshold)

    for null_threshold in null_thresholds:

        CS=Clustering(DS.SubjectPropertyBasket,DS.Subject_PropertyBasketCount,DS.PropertyUsageList,DS.Fpgrowth_list,support_threshold,null_threshold)

        PT=Partitioning(CS.Clusters,CS.Tables,DS.PropertyUsageList,null_threshold)

        tables_count=0
        for part in PT.Tables:
         if part is not None:
             tables_count+=1

        print("-----------------------------------")
        print(f"Support_Threshold: {support_threshold} \n Null_Threshold: {null_threshold} \n Number of tables: {tables_count} ")
        print("------------------------------------")  

# MP=Mapping(PT.Tables)
# gn=Generator()
# sql1="""select wpt.age2 , case when wpt.name='ferid' then wpt2.name else wpt.age1 end from wpt
#         join wpt2 ON wpt2.Subject1 = wpt.Subject1
#          where wpt.name<>'ferid' and wpt.age<>10"""
# sql="select wpt.age, wpt.test from wpt where wpt.name='ferid'"
# # print(gn.construct_join_statement(sql1))
# # print(gn.construct_query(sql))
# print(gn.find_columns(sql))




