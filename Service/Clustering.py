from Utils.Formulas import Formulas

class Clustering:

    def __init__(self,SubjectPropertyBasket,PropertyUsage,Support_Threshold,Null_Threshold):

        self.SubjectPropertyBasket=SubjectPropertyBasket
        self.PropertyUsage=PropertyUsage
        self.Support_Threshold=Support_Threshold
        self.Null_Threshold=Null_Threshold
        self.Clusters,self.Tables=self.find_Clusters()
        self.initialize()

    # private functions 
    def find_Clusters(self):
        Baskets=[]
        Binary_Tables=[]
        Basket_length=len(self.SubjectPropertyBasket)
        for key,value in self.SubjectPropertyBasket.items():
            if (value/Basket_length)*100>=self.Support_Threshold:
                Baskets.append(key)
            else:
                Binary_Tables.append(key)
        
        return Baskets,Binary_Tables
    
    def initialize(self):
        Removed_Indexes=[]
        for c1 in range(len(self.Clusters)):
            Is_Final=False
            if Formulas.null_percentage(self.Clusters[c1],self.PropertyUsage)<=self.Null_Threshold:
                Is_Final=True
                for c2 in range(len(self.Clusters)):
                    if c1!=c2 and set(self.Clusters[c1]).isdisjoint(self.Clusters[c2]):
                        Is_Final=False
            
            if Is_Final:
                self.Tables.append(self.Clusters[c1])
                Removed_Indexes.append(c1)
        
        for index in Removed_Indexes:
            self.Clusters.remove(index)
        
                
        
        
    
    # end private functions
        
