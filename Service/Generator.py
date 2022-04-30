import re

class Generator:
    def __init__(self):
        pass

    #--- private functions-----
    def find_columns(query):
        return re.findall(r'(?:(?i)WHERE|SELECT|AND|OR|GROUP BY|ORDER BY) \(?([a-zA-Z0-9.,]+)', query)