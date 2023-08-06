from pyspark.sql import SparkSession
import os
import config

from pyspark.sql.functions import pandas_udf, PandasUDFType
import pyspark.sql.functions as f
import pandas as pd


def apply(spark: SparkSession):
    # inferSchema = true, so that it can successfully infer data types (otherwise, it will set all columns as strings)
    # https://stackoverflow.com/questions/29725612/spark-csv-data-source-infer-data-types
    ds = spark.read.option("header", "true").option("inferSchema", "true").csv(
        os.path.join(config.ROOT_DIR, 'data/sensors.csv'))
    ds.printSchema()

    # why using spark built-in rather than custom pandas UDF? https://stackoverflow.com/questions/37580782/pyspark-collect-set-or-collect-list-with-groupby

    # how to use the collect_list when the result of groupby produces several columns?
    # https://stackoverflow.com/questions/46807776/how-to-retrieve-all-columns-using-pyspark-collect-list-functions/46812533

    # group by id an sensor, then, for each group, calculate avg temperature
    # then, apply pandas udf to generate one column per sensor type

    # ALTERNATIVE 1 (first selecting id and sensor and avgTemperature in a struct), then agg... collect_list on the struct
    # grouped_by_id_collected = ds.groupBy("id", "sensor")\
    #     .agg(f.avg("temperature").alias("avgTemperature"))\
    #     .select("id", f.struct(["sensor", "avgTemperature"]).alias("l"))\
    #     .groupBy("id").agg(f.collect_list("l"))

    # ALTERNATIVE 2 (directly specify the struct in collect_list)
    grouped_by_id_collected = ds.groupBy("id", "sensor") \
        .agg(f.avg("temperature").alias("avgTemperature")) \
        .groupBy("id").agg(f.collect_list(f.struct(["sensor", "avgTemperature"])).alias("l"))

    grouped_by_id_collected.show(truncate=False)
    grouped_by_id_collected.printSchema()

    # On the use of higher order functions:
    # https://docs.databricks.com/delta/data-transformation/higher-order-lambda-functions.html
    # https://docs.databricks.com/_static/notebooks/higher-order-functions-tutorial-python.html
    # https://www.waitingforcode.com/apache-spark-sql/apache-spark-2.4.0-features-array-higher-order-functions/read
    # https://medium.com/@fqaiser94/manipulating-nested-data-just-got-easier-in-apache-spark-3-1-1-f88bc9003827 (ONLY IN 3.1.1)
    # https://docs.databricks.com/spark/latest/dataframes-datasets/complex-nested-data.html

    grouped_by_id_collected \
        .withColumn("avgTempTanque", f.expr("filter(l, x -> x.sensor == 'tanque')")) \
        .withColumn("avgTempTanque", f.expr("transform(avgTempTanque, x -> x.avgTemperature)[0]")) \
        .withColumn("avgTempPasteurizador", f.expr("filter(l, x -> x.sensor == 'pasteurizador')")) \
        .withColumn("avgTempPasteurizador", f.expr("transform(avgTempPasteurizador, x -> x.avgTemperature)[0]")) \
        .select("id", "avgTempTanque", "avgTempPasteurizador") \
        .show()
