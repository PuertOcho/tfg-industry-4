from pyspark.sql import SparkSession
import os
import config

def apply(spark: SparkSession):
    spark.read.format("mongo").load()\
        .drop("_id", "_msgid")\
        .coalesce(1)\
        .write.option("header", "true")\
        .csv(os.path.join(config.ROOT_DIR, 'data/sensors'))
