
from Service.Parser import Parser

class DataStructures:
    def __init__(self,QuerySets) -> None:
        self.QuerySets=QuerySets
        self.all_columns=["name","surname","age","phone","website"]  # here will calculate all distinct attributes
        
    
    #---- private functions -----

    def generate_attribute_usage_matrix(self,columns):
        attribute_usage_matrix=[]
        for column in columns:

            query_matrix=[]

            for element in self.all_columns:
                if element in column:
                    query_matrix.append(1)
                else:
                    query_matrix.append(0)

            attribute_usage_matrix.append(query_matrix)
        
        return attribute_usage_matrix
    
    def generate_attribute_affinity_matrix(self,usage_matrix):

        n_attributes=len(self.all_columns)
        n_queries=len(self.QuerySets)
        
        affinity_matrix=[[0 for i in range(n_attributes)] for j in range(n_attributes)] # defining zero values

        for i in range(n_attributes):
            for j in range(n_attributes):
                for q in range(n_queries):
                    if usage_matrix[q][i]==1 and usage_matrix[q][j]==1:
                        affinity_matrix[i][j]= affinity_matrix[i][j]+1

        return affinity_matrix
                


    


    #--- end of private functions -----
    