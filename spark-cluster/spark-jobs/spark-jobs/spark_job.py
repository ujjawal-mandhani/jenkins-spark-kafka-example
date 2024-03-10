from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import *
import re

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "invoice"

spark = SparkSession.builder\
  .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
  .appName("write_test_stream").getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark.read.option("header", "true").csv("/home/spark-jobs/organisation_data.csv")
# df_json = df.toJSON()
# arry = df_json.collect()
# final_arry = []
# for item in arry:
#     final_arry.append([item])
# df = spark.createDataFrame(final_arry, ["value"])
df = df.selectExpr("replace(upper(trim(country)), ' ', '') as key", "to_json(struct(*)) as value")
print(":::::::starting writing in kafka")
df.selectExpr("key", "value").write \
  .format("kafka") \
  .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
  .option("topic", KAFKA_TOPIC) \
  .save()

print(":::::::completed writing in kafka")
spark.stop()