from Utils.Helper import Helper 
from Utils.DataStructures import DataStructures
from Utils.DBContext import DbContext

# print("---Application is starting------")

# print("---CSV is importing--------")

# DbContext.Save_Csv_To_Sql()

# print("---End of importing------")

# print("----Metrics calculation------------")

# columns=Helper.GetColumnInformation()
# Helper.CalculateMetrics(columns)

# print("----End of metrics calculation------------")

columns=Helper.GetColumnInformation()
print(Helper.SubjectPropertyBasket(columns=columns)[5])

