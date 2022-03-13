from Utils.Helper import Helper

class DataStructures:

    def __init__(self):
        self.PropertyUsageList=self.find_PropertyUsageList()
        self.SubjectPropertyBasket=self.find_SubjectPropertyBasket()
    
    #-----------------Private methods-----------------------------------
    def find_PropertyUsageList(self):
        self.PropertyUsageList=Helper.Select("SELECT Column_Name as Name,Null_Count as Count FROM METRICS ORDER BY NULL_COUNT")
        return self.PropertyUsageList
    

    def find_SubjectPropertyBasket(self):
        pass

    #-------------End of private methods --------------------------------------


