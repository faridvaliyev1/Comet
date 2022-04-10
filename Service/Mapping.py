import imp
from importlib.abc import TraversableResources
from Utils.DBContext import DbContext

class Mapping:
    def __init__(self,Tables):
        self.Tables=Tables
        self.from_tuple_to_sql()

    #----------private functions--------------

    def from_tuple_to_sql(self):
        for item in self.Tables:
            print(item)
    
    #---------end of private functions--------