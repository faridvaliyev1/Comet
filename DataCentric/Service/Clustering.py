from Utils.Formulas import Formulas

class Clustering:

    def __init__(self,SubjectPropertyBasket,Subject_PropertyBasketCount,PropertyUsage,FpGrowth_List,Support_Threshold,Null_Threshold):
        self.SubjectPropertyBasket=SubjectPropertyBasket
        self.FpGrowth_List=FpGrowth_List
        self.Subject_PropertyBasketCount=Subject_PropertyBasketCount
        self.PropertyUsage=PropertyUsage
        self.Support_Threshold=Support_Threshold
        self.Null_Threshold=Null_Threshold
        self.Clusters,self.Tables=self.find_Clusters()
        # print("start point of clustering")
        
        self.initialize()
        

        
    # private functions 

    # Getting clusters and final tables from the given SubjectPropertybasket
    # Function returns Clusters which will given to the next step and final tables
    def find_Clusters(self):
        Baskets=[]
        Binary_Tables=[]
        for key,value in self.FpGrowth_List.items():
            if not self.check_if_Subset(set(key),Baskets):
                Baskets.append(key)
        
        for key,value in self.Subject_PropertyBasketCount.items():
            result=self.find_nonintersection(set(key),Baskets)
            result_table=self.find_nonintersection(result,Binary_Tables)
            
            if len(result_table)>0:
                Binary_Tables.append(tuple(result_table))
        
        return Baskets,Binary_Tables
    
    def find_nonintersection(self,Key,Basket):
        for element in Basket:
            Key=(Key^set(element))&Key
        return Key

    def check_if_Subset(self,Key,Basket):
        for element in Basket:
            if Key.issubset(element):
                return True
        
        return False
    
    def check_if_Disjoint(self,Key,Baskets):
        for element in Baskets:
            if Key.isdisjoint(element):
                return True
        
        return False
    
    def find_Unique_Properties(self,Baskets):
        Unique_Properties=[]
        for basket in Baskets:
            for item in basket:
                if item not in Unique_Properties:
                    Unique_Properties.append(item)
        
        return Unique_Properties
            

    # This is setting up all the Clustering step
    def initialize(self):
        Removed_Indexes=[]
        
        for c1 in range(len(self.Clusters)):
            Is_Final=False
            if Formulas.null_percentage(self.Clusters[c1],self.PropertyUsage)<=self.Null_Threshold:
                
                Is_Final=True
                for c2 in range(len(self.Clusters)):
                    
                    if c1!=c2 and (set(self.Clusters[c1]) & set(self.Clusters[c2])):
                        Is_Final=False
                        break
            
            if Is_Final:
                self.Tables.append(self.Clusters[c1])
                Removed_Indexes.append(c1)
        
        for index in sorted(Removed_Indexes,reverse=True):
            del self.Clusters[index]
        
    
    # end private functions
        
