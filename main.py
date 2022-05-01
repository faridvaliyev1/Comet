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

DbContext.Save_Csv_To_Sql("Data/wpt.csv")

print("---End of importing------")

print("----Metrics calculation------------")

columns=Helper.GetColumnInformation()
Helper.CalculateMetrics(columns)

print("----End of metrics calculation------------")

# DS=DataStructures(Configurations.SUPPORT_THRESHOLD)

# CS=Clustering(DS.SubjectPropertyBasket,DS.Subject_PropertyBasketCount,DS.PropertyUsageList,DS.Fpgrowth_list,Configurations.SUPPORT_THRESHOLD,Configurations.NULL_THRESHOLD)

# PT=Partitioning(CS.Clusters,CS.Tables,DS.PropertyUsageList,Configurations.NULL_THRESHOLD)

# MP=Mapping(PT.Tables)
gn=Generator()
sql="""select wpt.age2 , case when wpt.name='ferid' then wpt.name1 else wpt.age1 end from wpt
        join wpt2 ON wpt2.Subject1 = wpt.Subject1
         where wpt.name<>'ferid' and wpt.age<>10"""

print(gn.construct_query(sql))


