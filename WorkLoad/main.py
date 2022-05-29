# from Service.Parser import Parser

# parser=Parser(["select name from wpt where wpt.full_name='ferid' GROUP BY wpt.age1 , wpt.name1",
#                 "select wpt.name , wpt.age from wpt where wpt.city='test'"])
# print(parser.parse_columns())
from Utils.DataStructures import DataStructures
import numpy as np

columns=[    ["name","surname"]
            ,["name","age","phone"]
            ,["age","phone"]
            ,["age","website"]   
                                 ]

DS=DataStructures(columns)

aum= DS.generate_attribute_usage_matrix(columns)


aam=DS.generate_attribute_affinity_matrix(aum)

print(np.matrix(aam))