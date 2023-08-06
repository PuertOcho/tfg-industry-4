from pyspark.sql import SparkSession
import os
import config
from pyspark.sql.functions import lit
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pyspark.sql.functions as f
from pyspark.sql.functions import explode
import pandas as pd
from pyspark_getting_started import groupby_input_mllib


def apply(spark: SparkSession, path):

    df_raw_correct = spark.read.option("header", "true").option("inferSchema", "true").json(
        os.path.join(config.ROOT_DIR, 'data/train/data_correct/data.json'))
    df_correct = groupby_input_mllib.apply(df_raw_correct).withColumn('goodness', lit(1))

    #print('train_data_correct ------------------------')
    #print("df_correct: " + str(df_correct.count()))
    #df_correct.show(n=10)
    #df_correct.printSchema()

    df_raw_error = spark.read.option("header", "true").option("inferSchema", "true").json(
        os.path.join(config.ROOT_DIR, 'data/train/data_error/data.json'))
    df_error = groupby_input_mllib.apply(df_raw_error).withColumn('goodness', lit(0))

    #print('train_data_error ------------------------')
    #print("df_error: " + str(df_error.count()))
    #df_error.filter("task == 'CB'").show(n=10)

    df_res = df_correct.union(df_error)
    #print("Union: " + str(df_res.count()))

    df_res.coalesce(1).write.json(os.path.join(config.ROOT_DIR, path), mode="overwrite")