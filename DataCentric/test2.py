from pickle import TRUE
from re import I
from psycopg2 import connect
from Utils.Helper import Helper 
from Utils.DataStructures import DataStructures
from Utils.DBContext import DbContext

from Service.Clustering import Clustering
from Service.Mapping import Mapping
from Service.Partitioning import Partitioning
from Service.Generator import Generator
from Service.StarPattern import StarPattern
from Configurations import NULL_THRESHOLD

DbContext.Save_Csv_To_Sql("Data/combined_100M.csv")
