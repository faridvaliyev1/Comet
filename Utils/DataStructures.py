from Utils.DBContext import DbContext
from Utils.Helper import Helper
from collections import Counter
from apriori_python import apriori
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth

class DataStructures:

    def __init__(self):
        self.PropertyUsageList=self.find_PropertyUsageList()
        self.SubjectPropertyBasket=self.find_SubjectPropertyBasket()
        self.Subject_PropertyBasketCount=self.find_Property_UsageCount()
        self.Apriori_List=self.find_apriori()
        self.Fpgrowth_list=self.find_fpgrowth()
    
    #-----------------Private methods-----------------------------------
    def find_PropertyUsageList(self):
        properties=DbContext.Select("SELECT Column_Name as Name,Not_Null_Count as Count FROM METRICS ORDER BY Not_Null_Count DESC")
        
        self.PropertyUsageList=dict((key,value) for key,value in properties) # converting to dictionary for O(1) lookup
        return self.PropertyUsageList
    

    def find_SubjectPropertyBasket(self):
        columns=Helper.GetColumnInformation()
        return Helper.SubjectPropertyBasket(columns=columns)

    def find_Property_UsageCount(self):
        return Counter(tuple(item) for item in self.SubjectPropertyBasket.values())
    
    # apriori algorithm
    def find_apriori(self):
        apriori_list=[value for key,value in self.SubjectPropertyBasket.items()]
        freqItemSet, rules = apriori(apriori_list, minSup=0.5, minConf=0.5)
        return freqItemSet,rules
    
    def find_fpgrowth(self):
        fpgrowth_list=[value for key,value in self.SubjectPropertyBasket.items()]
        te=TransactionEncoder()
        te_ary=te.fit(fpgrowth_list).transform(fpgrowth_list)
        df=pd.DataFrame(te_ary,columns=te.columns_)
        return fpgrowth(df, min_support=0.5)

    
    #-------------End of private methods --------------------------------------

    
 
            



