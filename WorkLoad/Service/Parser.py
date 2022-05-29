import re
class Parser:
    def __init__(self,queries) -> None:
        self.queries=queries
        self.columns=self.parse_columns()
        self.distinct_columns=self.parse_distinct_columns()

    
    def parse_columns(self):
        columns=[]
        for query in self.queries:
            column=self.find_columns(query)
            columns.append(column)

        return columns

    def find_columns(self,query):
        columns=re.findall(r'(?:(?i)WHERE|SELECT|AND|OR|GROUP BY|ORDER BY|THEN|ELSE|CASE WHEN|ON|=) \(?([a-zA-Z0-9._,]+)',query)
        for index in range(len(columns)):
            if "." in columns[index]:
                columns[index]=columns[index].split('.')[1]

        return columns

    def parse_distinct_columns(self):
        distinct_columns=[]
        for elements in self.columns:
            for element in elements:
                if element not in distinct_columns:
                    distinct_columns.append(element)

                
