from pyspark.sql import SparkSession, DataFrame
import os
import config
import pyspark.sql.functions as f
from pyspark.sql.functions import explode
from pyspark.sql.functions import lit


#def apply(spark: SparkSession, path):
def apply(df: DataFrame):

    grouped_by_task_id_factory = df.groupBy("task", "milktank").agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("preasure").alias("minPreasure"),
        f.max("preasure").alias("maxPreasure"),
        f.avg("preasure").alias("avgPreasure")) \
        .filter((df.task == "CB") | (df.task == "CC") | (df.task == "CD") | (df.task == "CE")) \
        .withColumn("minHumidity", lit(None)) \
        .withColumn("maxHumidity", lit(None)) \
        .withColumn("avgHumidity", lit(None))

    grouped_by_task_order_collected_transport_1 = df.filter("task == 'B'").groupBy("task", "order").agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("humidity").alias("minHumidity"),
        f.max("humidity").alias("maxHumidity"),
        f.avg("humidity").alias("avgHumidity")) \
        .na.drop(how='any')

    grouped_by_task_order_collected_transport_2 = df.filter("task == 'D'").groupBy("task", "order").agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("humidity").alias("minHumidity"),
        f.max("humidity").alias("maxHumidity"),
        f.avg("humidity").alias("avgHumidity")) \
        .na.drop(how='any')

    map_order_milkTanks = df.filter("task == 'AB'").select("order",
                                                           explode("milkTanks").alias("milkTank")).na.drop(
        how='any')

    map_order_pallets = df.filter("task == 'EA'").select("order", explode("pallets").alias("milkTank")).na.drop(
        how='any')

    filter_B_transport_task = map_order_milkTanks.join(
        grouped_by_task_order_collected_transport_1,
        grouped_by_task_order_collected_transport_1.order == map_order_milkTanks.order,
        "full").drop("order")

    filter_D_transport_task = map_order_pallets.join(
        grouped_by_task_order_collected_transport_2,
        grouped_by_task_order_collected_transport_2.order == map_order_pallets.order,
        "full").drop("order")

    union_transports = filter_B_transport_task.union(filter_D_transport_task) \
        .withColumn("minPreasure", lit(None)) \
        .withColumn("maxPreasure", lit(None)) \
        .withColumn("avgPreasure", lit(None))

    df_res = grouped_by_task_id_factory.join(union_transports,
                                             ['task',
                                              'milktank',
                                              'minTemperature',
                                              'maxTemperature',
                                              'avgTemperature',
                                              'minPreasure',
                                              'maxPreasure',
                                              'avgPreasure',
                                              'minHumidity',
                                              'maxHumidity',
                                              'avgHumidity'], "full")
    return df_res
