from pyspark.sql import SparkSession
import os
import config

from pyspark.sql.functions import pandas_udf, PandasUDFType
import pyspark.sql.functions as f
import pandas as pd

# WARNING Only works with Spark 3.0.1

# a pdf might be empty, and that could mean several things
# https://stackoverflow.com/questions/24652417/how-to-check-if-pandas-series-is-empty
def is_empty_nans(pdf):
    return pdf.dropna(how='all').empty

# mirar tambien: https://intellipaat.com/community/11611/applying-udfs-on-groupeddata-in-pyspark-with-functioning-python-example

def apply(spark: SparkSession):

    # key: the id of this group
    # pdf: the values inside this group
    @pandas_udf("id string, temperature double", PandasUDFType.GROUPED_MAP)
    def mean_custom(pdf: pd.DataFrame):
        key = pdf['id'].iloc[0]
        mean = pdf['temperature'].mean()
        #print(key)
        #print(mean)
        return pd.DataFrame([[key] + [mean]])

    @pandas_udf("id string, avgTempTanque double, avgTempPasteurizador double", PandasUDFType.GROUPED_MAP)
    def avg_temperature_by_sensor(pdf: pd.DataFrame):
        key = pdf['id'].iloc[0]

        tanque = pdf.loc[pdf['sensor'] == 'tanque']['avgTemperature']
        pasteurizador = pdf.loc[pdf['sensor'] == 'pasteurizador']['avgTemperature']
        # print(tanque)
        # print(pasteurizador)

        # workaround: cast panda series to float to avoid troubles with spark arrow (https://spark.apache.org/docs/2.4.0/sql-pyspark-pandas-with-arrow.html)

        #return pd.DataFrame([[key] + [None if tanque is None else float(tanque)] + [None if pasteurizador is None else float(pasteurizador)]])

        return pd.DataFrame([[key] + [float(tanque) if not is_empty_nans(tanque) else None] + [float(pasteurizador) if not is_empty_nans(pasteurizador) else None]])

    # inferSchema = true, so that it can successfully infer data types (otherwise, it will set all columns as strings)
    # https://stackoverflow.com/questions/29725612/spark-csv-data-source-infer-data-types
    ds = spark.read.option("header", "true").option("inferSchema", "true").csv(os.path.join(config.ROOT_DIR, 'data/sensors.csv'))
    ds.printSchema()

    basic_udf_example = ds.groupBy("id").apply(mean_custom)

    basic_udf_example.show()

    # group by id an sensor, then, for each group, calculate avg temperature
    # then, apply pandas udf to generate one column per sensor type
    avg_temperature_by_id = ds.groupBy("id", "sensor")\
        .agg(f.avg("temperature").alias("avgTemperature"))\
        .groupBy("id").apply(avg_temperature_by_sensor)

    avg_temperature_by_id.show()