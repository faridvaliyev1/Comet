from operator import imod
from pyspark import SparkContext

DATABASE_NAME="cometdb"
DATABASE_USER="postgres"
DATABASE_PASSWORD="ferid"
DATABASE_HOST="127.0.0.1"
DATABASE_PORT="5433"

SUPPORT_THRESHOLD=0.2
NULL_THRESHOLD=10

# sc=SparkContext("local","Comet")
# words=sc.parallelize(
#     ["scala",
#      "java",
#      "hadoop",
#      "akka",
#      "sparksql"]
# )
# counts=words.count()
# print("Number of elements in RDD",counts)

CONNECTION_CONFIG_DICT={
    'database':DATABASE_NAME, 
    'user':DATABASE_USER, 
    'password':DATABASE_PASSWORD, 
    'host':DATABASE_HOST, 
    'port': DATABASE_PORT
}

DATABASE_ENGINE=f"""postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:{DATABASE_PORT}/{DATABASE_NAME}"""