from Utils.DBContext import DbContext
from Utils.Helper import Helper
from collections import Counter

class DataStructures:

    def __init__(self):
        self.PropertyUsageList=self.find_PropertyUsageList()
        self.SubjectPropertyBasket=self.find_SubjectPropertyBasket()
        self.Subject_PropertyBasketCount=self.find_Property_UsageCount()
    
    #-----------------Private methods-----------------------------------
    def find_PropertyUsageList(self):
        self.PropertyUsageList=DbContext.Select("SELECT Column_Name as Name,Null_Count as Count FROM METRICS ORDER BY NULL_COUNT")
        return self.PropertyUsageList
    

    def find_SubjectPropertyBasket(self):
        columns=Helper.GetColumnInformation()
        return Helper.SubjectPropertyBasket(columns=columns)

    def find_Property_UsageCount(self):
        return Counter(tuple(item) for item in self.SubjectPropertyBasket.values())

    #-------------End of private methods --------------------------------------

 
            



