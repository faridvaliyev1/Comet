class Clustering:

    def __init__(self,SubjectPropertyBasket,PropertyUsage,Support_Threshold,Null_Threshold):

        self.SubjectPropertyBasket=SubjectPropertyBasket
        self.PropertyUsage=PropertyUsage
        self.Support_Threshold=Support_Threshold
        self.Null_Threshold=Null_Threshold
        self.Clusters,self.Binary_Tables=self.find_Clusters()
    

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
