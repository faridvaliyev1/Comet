from Service.Parser import Parser

class DataStructures:
    def __init__(self,QuerySets) -> None:
        self.QuerySets=QuerySets
    
    #---- private functions -----

    def generate_attribute_usage_matrix(self):
        attribute_usage_matrix=[]
        for query in self.QuerySets:

            query_matrix=[]

            columns=Parser.parse_columns(query)
            all_columns=Parser.parse_distinct_columns()

            for column in all_columns:
                if column in columns:
                    query_matrix.append(1)
                else:
                    query_matrix.append(0)

            attribute_usage_matrix.append(query_matrix)
        
        return attribute_usage_matrix

            
                


    


    #--- end of private functions -----
    