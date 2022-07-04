# from Service.Parser import Parser

# parser=Parser(["select name from wpt where wpt.full_name='ferid' GROUP BY wpt.age1 , wpt.name1",
#                 "select wpt.name , wpt.age from wpt where wpt.city='test'"])
# print(parser.parse_columns())
from Utils.DataStructures import DataStructures
from Helper.Helper import Helper
import numpy as np

columns=Helper.get_workloads()
# ["name","surname","age","phone","website"]
DS=DataStructures(columns)


aum= DS.generate_attribute_usage_matrix(columns)
print(aum)

aam=DS.generate_attribute_affinity_matrix(aum)
print(aam)
# bea=DS.BEA(aam)

# print(bea)
