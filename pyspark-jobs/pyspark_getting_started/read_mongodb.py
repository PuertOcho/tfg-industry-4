import pandas
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pyspark.sql.functions as f

"""
Receives a SparkSession object previously configured:
- "spark.mongodb.input.uri"
- "spark.mongodb.output.uri"
"""

def apply(spark: SparkSession):
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    return df
