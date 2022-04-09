class Formulas:
    
    def metric_total_null(total_nulls,column,row):
        return total_nulls/(column*row)
    
    def metric_total_null_column(total_nulls,column):
        return total_nulls/column
    
    def metric_total_null_row(total_nulls,row):
        return total_nulls/row
    
    def null_percentage(Cluster,PropertyUsage):
        Cluster_length=len(Cluster)
        Cluster_max_count=PropertyUsage[Cluster[0]]
        PropertyUsage_Sum=0
       
        for property in Cluster:
            if Cluster_max_count<PropertyUsage[property]:
                Cluster_max_count=PropertyUsage[property]
            
            PropertyUsage_Sum+=PropertyUsage[property]
        
        cluster_null_percentage= ((Cluster_length*Cluster_max_count-PropertyUsage_Sum)/(Cluster_length+1)*Cluster_max_count)
        
        return cluster_null_percentage
        
        
        
        
        
            
        
        
