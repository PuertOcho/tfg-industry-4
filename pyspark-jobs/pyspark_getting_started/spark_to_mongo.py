from pyspark.sql import SparkSession
import os
import config

def apply(spark: SparkSession, path):
    spark.read.format("mongo").load()\
        .coalesce(1)\
        .write.option("header", "true")\
        .json(os.path.join(config.ROOT_DIR, path))
