from Utils.Formulas import Formulas
class Partitioning:
    def __init__(self,Clusters,PropertyUsage,Null_Threshold):

        self.Null_Threshold=Null_Threshold
        self.Clusters=Clusters
        self.PropertyUsage=PropertyUsage
        self.Tables=[]

    #--- start of private functions
    def initialize(self):
        for cluster in self.Clusters:
            self.Clusters.remove(cluster)
            if Formulas.null_percentage(cluster,self.PropertyUsage)>self.Null_Threshold:
                while Formulas.null_percentage(cluster,self.PropertyUsage)<=self.Null_Threshold:
                    p=self.PropertyUsage[len(self.PropertyUsage)-1]
                    print(p)
                    

            self.Tables.append(cluster)
            for cluster2 in self.Clusters:
                cluster2=set(cluster2).difference(set(cluster))
    
    #end of private functions
        
        
            


