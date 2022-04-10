from Utils.Formulas import Formulas
class Partitioning:
    def __init__(self,Clusters,Tables,PropertyUsage,Null_Threshold):

        self.Null_Threshold=Null_Threshold
        self.Clusters=Clusters
        self.PropertyUsage=PropertyUsage
        self.Tables=Tables
        self.initialize()
        
        

    #--- start of private functions
    
    # initializing the partitioning part
    def initialize(self):
        
        for cluster in self.Clusters:
            
            self.Clusters.remove(cluster)
            
            if Formulas.null_percentage(cluster,self.PropertyUsage)>self.Null_Threshold:
                
                while Formulas.null_percentage(cluster,self.PropertyUsage)>self.Null_Threshold:
                    
                    index,property=self.find_most_nullable_property(cluster)
                    
                    cluster_list=list(cluster)
                    cluster_list.remove(property)
                    cluster=tuple(cluster_list)
                    if not self.property_exist(property):
                        self.Tables.append((property))
                    
            self.Tables.append(cluster)
            for index in range(len(self.Clusters)):
                cluster2=self.Clusters[index]
                self.Clusters[index]=list(set(cluster2).difference(set(cluster)))
        
        for cluster in self.Clusters:
            self.Tables.append(tuple(cluster))
                
        
    # Finding the property which is causing the most null values 
    # Function returns index of the property in the cluster and as well as its name
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
    
    # Finding whether the property is exist in the lower support cluster
    def property_exist(self,property):
        for cluster in self.Clusters:
            if property in cluster:
                return True
        
        return False

    #end of private functions
        
        
            


