from numpy import column_stack
from Service.Mapping import Mapping
from Service.Partitioning import Partitioning
from Utils.Helper import Helper 
from Utils.DataStructures import DataStructures
from Utils.DBContext import DbContext
from Service.Clustering import Clustering
import Configurations


print("---Application is starting------")

print("---CSV is importing--------")

DbContext.Save_Csv_To_Sql("Data/fake.csv")

print("---End of importing------")

print("----Metrics calculation------------")

columns=Helper.GetColumnInformation()
Helper.CalculateMetrics(columns)

print("----End of metrics calculation------------")

DS=DataStructures(Configurations.SUPPORT_THRESHOLD)

CS=Clustering(DS.SubjectPropertyBasket,DS.Subject_PropertyBasketCount,DS.PropertyUsageList,DS.Fpgrowth_list,Configurations.SUPPORT_THRESHOLD,Configurations.NULL_THRESHOLD)

PT=Partitioning(CS.Clusters,CS.Tables,DS.PropertyUsageList,Configurations.NULL_THRESHOLD)

MP=Mapping(PT.Tables)




