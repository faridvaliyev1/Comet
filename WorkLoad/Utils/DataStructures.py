import numpy as np
from Service.Parser import Parser

class DataStructures:
    def __init__(self,QuerySets) -> None:
        self.QuerySets=QuerySets
        
        self.all_columns=["name","surname","age","phone","website"]  # here will calculate all distinct attributes
        
        self.usage_matrix=self.generate_attribute_usage_matrix(self.QuerySets)
        self.affinity_matrix=self.generate_attribute_affinity_matrix(self.usage_matrix)
    
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
        
        affinity_matrix=np.zeros((n_attributes,n_attributes))

        for i in range(n_attributes):
            for j in range(n_attributes):
                for q in range(n_queries):
                    if usage_matrix[q][i]==1 and usage_matrix[q][j]==1:
                        affinity_matrix[i][j]= affinity_matrix[i][j]+1

        return affinity_matrix
    
    def dot_prod(self,vec_a, vec_b):
        return np.dot(vec_a.flatten(), vec_b.flatten())

    def BEA(self,aa_matrix):
        cc_matrix = aa_matrix[:, :2]
        cc_matrix = np.append(np.zeros((len(self.all_columns),1)), cc_matrix, axis=1)
        cc_matrix = np.append(cc_matrix,np.zeros((len(self.all_columns),1)), axis=1)

        # BOND ENERGY ALGORITHM - CC_MATRIX GENERATION
        for k in range(2, len(aa_matrix)):
            i, j = 0, 1
            get_values = []
            while j < cc_matrix.shape[1]:
                print(i,k,j, len(cc_matrix))
                get_values.append(2 * self.dot_prod(cc_matrix[:, i:i+1], aa_matrix[:, k:k+1]) + 
                                2 * self.dot_prod(aa_matrix[:, k:k+1], cc_matrix[:, j:j+1]) - 
                                2 * self.dot_prod(cc_matrix[:, i:i+1], cc_matrix[:, j:j+1]))  
                i = j
                j+=1
        pos = np.argmax(get_values) + 1
        cc_matrix = np.insert(cc_matrix, pos, aa_matrix[k:k+1], axis=1)

        # BOND ENERGY ALGORITHM - REMOVES ZEROS COLUMNS
        cc_matrix = np.delete(cc_matrix, 0, axis=1)
        cc_matrix = np.delete(cc_matrix, cc_matrix.shape[1]-1, axis=1)

        return cc_matrix
    


    #--- end of private functions -----
    