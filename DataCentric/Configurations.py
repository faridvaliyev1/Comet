from operator import imod
from pyspark import SparkContext

DATABASE_NAME="wellmate"
DATABASE_USER="wellmate"
DATABASE_PASSWORD="wellmate123"
DATABASE_HOST="localhost"
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