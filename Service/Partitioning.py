from Utils.Formulas import Formulas
class Partitioning:
    def __init__(self,Clusters,PropertyUsage,Null_Threshold):

        self.Null_Threshold=Null_Threshold
        self.Clusters=Clusters
        self.PropertyUsage=PropertyUsage
        self.Tables=[]
        self.initialize()

    #--- start of private functions
    def initialize(self):
        
        for cluster in self.Clusters:
            print(self.find_most_nullable_property(cluster))
            self.Clusters.remove(cluster)
            
            if Formulas.null_percentage(cluster,self.PropertyUsage)>self.Null_Threshold:
                while Formulas.null_percentage(cluster,self.PropertyUsage)<=self.Null_Threshold:
                    index,property=self.find_most_nullable_property(cluster)
                    cluster.pop(index)
                    
            self.Tables.append(cluster)
            for cluster2 in self.Clusters:
                cluster2=set(cluster2).difference(set(cluster))
        
    
    def find_most_nullable_property(self,Cluster):
        
        minimum=self.PropertyUsage[Cluster[0]]
        index=0
        minimum_property=Cluster[0]
        for i in range(len(Cluster)):
            if minimum>self.PropertyUsage[Cluster[i]]:
                minimum=self.PropertyUsage[Cluster[i]]
                minimum_property=Cluster[i]
                index=i
        
        return index,minimum_property

            
    
    #end of private functions
        
        
            


