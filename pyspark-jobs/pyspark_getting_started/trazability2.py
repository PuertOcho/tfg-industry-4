import json

from pyspark.sql import SparkSession
import os
import config
import cloudpickle as pickle

from pyspark.sql.functions import pandas_udf, PandasUDFType
import pyspark.sql.functions as f
from pyspark.sql.functions import explode
import pandas as pd
from pyspark.sql.functions import min
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType


def apply(spark: SparkSession, ID):
    # inferSchema = true, so that it can successfully infer data types (otherwise, it will set all columns as strings)
    # https://stackoverflow.com/questions/29725612/spark-csv-data-source-infer-data-types
    # array_contains(df("languages"),"Java")

    ID = "PH27A59CC2"
    ds = spark.read.option("header", "true").option("inferSchema", "true").json(
        os.path.join(config.ROOT_DIR, 'data/sensors_complete_data_json/data.json'))
    ds.printSchema()

    task_CB_CC_CD_CE = ds.filter(f.col('id') == ID)

    task_AA_AB_CA = ds.filter(f.array_contains(ds.milkTanks, ID))  # AA AB CA

    order_t1 = task_AA_AB_CA.filter(task_AA_AB_CA.task == 'AB').select("order").first()[0]
    task_AB_B_CA = ds.filter(ds.order == order_t1)  # AB B CA

    task_CF_EA = ds.filter(f.array_contains(ds.pallets, ID))  # CF EA

    order_t2 = task_CF_EA.filter(task_CF_EA.task == 'EA').select("order").first()[0]
    task_CF_D_EA_EB = ds.filter(ds.order == order_t2)  # CF D EA EB

    # Etapa proveedor
    task_AA = \
    task_AA_AB_CA.filter(task_AA_AB_CA.task == 'AA').select('timestamp', 'supplier', 'worker', 'stage').collect()[0]
    task_AB = \
    task_AA_AB_CA.filter(task_AA_AB_CA.task == 'AB').select('timestamp', 'supplier', 'worker', 'order').collect()[0]

    # Etapa transporte 1
    task_B = task_AB_B_CA.filter(task_AB_B_CA.task == 'B').select('worker', 'transport', 'order', 'temperature',
                                                                  'humidity').collect()[0]
    task_B_metrics = task_AB_B_CA.filter(task_AB_B_CA.task == 'B').agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("humidity").alias("minHumidity"),
        f.max("humidity").alias("maxHumidity"),
        f.avg("humidity").alias("avgHumidity"),
        f.min("timestamp").alias("start_timestamp"),
        f.max("timestamp").alias("finish_timestamp")).collect()[0]

    # Etapa Fabricacion
    task_CA = task_AA_AB_CA.filter(task_AB_B_CA.task == 'CA').select('timestamp', 'worker', 'order').collect()[0]
    task_CB_CC_CD_CE_metrics = task_CB_CC_CD_CE.groupBy('task').agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("preasure").alias("minPreasure"),
        f.max("preasure").alias("maxPreasure"),
        f.avg("preasure").alias("avgPreasure"),
        f.min("timestamp").alias("start_timestamp"),
        f.max("timestamp").alias("finish_timestamp"))
    task_CB_metrics = task_CB_CC_CD_CE_metrics.filter(task_AB_B_CA.task == 'CB').collect()[0]
    task_CC_metrics = task_CB_CC_CD_CE_metrics.filter(task_AB_B_CA.task == 'CC').collect()[0]
    task_CD_metrics = task_CB_CC_CD_CE_metrics.filter(task_AB_B_CA.task == 'CD').collect()[0]
    task_CE_metrics = task_CB_CC_CD_CE_metrics.filter(task_AB_B_CA.task == 'CE').collect()[0]
    task_CF = task_CF_EA.filter(task_AB_B_CA.task == 'CF').collect()[0]

    # Etapa transporte 2
    task_D = task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'D').select('worker', 'transport', 'order', 'temperature',
                                                                     'humidity').collect()[0]
    task_D_metrics = task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'D').agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("humidity").alias("minHumidity"),
        f.max("humidity").alias("maxHumidity"),
        f.avg("humidity").alias("avgHumidity"),
        f.min("timestamp").alias("start_timestamp"),
        f.max("timestamp").alias("finish_timestamp")).collect()[0]

    # Etapa almacen
    task_EA = task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'EA').select('timestamp', 'worker', 'order').collect()[0]
    task_EB = \
    task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'EB').select('timestamp', 'worker', 'order', 'storage').collect()[0]

    print(ID)
    for i in task_EB.storage:
        if i.pallet == ID:
            task_EB_storage_hall = i.hall
            task_EB_storage_number = i.number
            task_EB_storage_pallet = i.pallet

    data = spark.createDataFrame([(ID, task_AA.timestamp, task_AA.supplier)])

    print(data._1)
    print(data._2)

    data.show()
    data.printSchema()

    schema = StructType([ \
        StructField("id", StringType(), True), \
        StructField("id2", TimestampType(), True), \
        StructField("id3", StringType(), True)])

    columns = ["id", "id2", "id3"]

    df = spark.createDataFrame(data).toDF()
    df.show()


'''
    data = [(
        ID,
        task_AA['timestamp'],
        task_AA['supplier'],
        task_AA['worker'], \
        task_AB['timestamp'],
        task_AB['supplier'],
        task_AB['worker'],
        task_AB['order'], \

             task_B_metrics.start_timestamp,
             task_B_metrics.finish_timestamp,
             task_B.worker,
             task_B.transport,
             task_B.order,
             task_B_metrics.minTemperature,
             task_B_metrics.maxTemperature,
             task_B_metrics.avgTemperature,
             task_B_metrics.minHumidity,
             task_B_metrics.maxHumidity,
             task_B_metrics.avgHumidity,

             task_CA.timestamp,
             task_CA.worker,
             task_CA.order,

             task_CB_metrics.start_timestamp,
             task_CB_metrics.finish_timestamp,
             task_CB_metrics.minTemperature,
             task_CB_metrics.maxTemperature,
             task_CB_metrics.avgTemperature,
             task_CB_metrics.minPreasure,
             task_CB_metrics.maxPreasure,
             task_CB_metrics.avgPreasure,

             task_CC_metrics.start_timestamp,
             task_CC_metrics.finish_timestamp,
             task_CC_metrics.minTemperature,
             task_CC_metrics.maxTemperature,
             task_CC_metrics.avgTemperature,
             task_CC_metrics.minPreasure,
             task_CC_metrics.maxPreasure,
             task_CC_metrics.avgPreasure,

             task_CD_metrics.start_timestamp,
             task_CD_metrics.finish_timestamp,
             task_CD_metrics.minTemperature,
             task_CD_metrics.maxTemperature,
             task_CD_metrics.avgTemperature,
             task_CD_metrics.minPreasure,
             task_CD_metrics.maxPreasure,
             task_CD_metrics.avgPreasure,

             task_CE_metrics.start_timestamp,
             task_CE_metrics.finish_timestamp,
             task_CE_metrics.minTemperature,
             task_CE_metrics.maxTemperature,
             task_CE_metrics.avgTemperature,
             task_CE_metrics.minPreasure,
             task_CE_metrics.maxPreasure,
             task_CE_metrics.avgPreasure,

             task_CF.timestamp,
             task_CF.worker,
             task_CF.order,

             task_D_metrics.start_timestamp,
             task_D_metrics.finish_timestamp,
             task_D.worker,
             task_D.transport,
             task_D.order,
             task_D_metrics.minTemperature,
             task_D_metrics.maxTemperature,
             task_D_metrics.avgTemperature,
             task_D_metrics.minHumidity,
             task_D_metrics.maxHumidity,
             task_D_metrics.avgHumidity,

             task_EA.timestamp,
             task_EA.worker,
             task_EA.order,

             task_EB.timestamp,
             task_EB.worker,
             task_EB.order,
             task_EB_storage_pallet,
             task_EB_storage_hall,
             task_EB_storage_number)
            ]

    schema = StructType([ \
        StructField("id", StringType(), True), \
        StructField("task_AA_timestamp", StringType(), True), \
        StructField("task_AA_supplier", StringType(), True), \
        StructField("task_AA_worker", StringType(), True), \
        StructField("task_AB_timestamp", StringType(), True), \
        StructField("task_AB_supplier", StringType(), True), \
        StructField("task_AB_worker", StringType(), True), \
        StructField("task_AB_order", StringType(), True), \
        StructField("task_B_start_timestamp", StringType(), True), \
        StructField("task_B_finish_timestamp", StringType(), True),
        StructField("task_B_worker", StringType(), True), \
        StructField("task_B_transport", StringType(), True), \
        StructField("task_B_order", StringType(), True), \
        StructField("task_B_minTemperature", StringType(), True), \
        StructField("task_B_maxTemperature", StringType(), True),
        StructField("task_B_avgTemperature", StringType(), True), \
        StructField("task_B_minHumidity", StringType(), True), \
        StructField("task_B_maxHumidity", StringType(), True), \
        StructField("task_B_avgHumidity", StringType(), True), \
        StructField("task_CA_timestamp", StringType(), True),
        StructField("task_CA_worker", StringType(), True), \
        StructField("task_CA_order", StringType(), True), \
        StructField("task_CB_start_timestamp", StringType(), True), \
        StructField("task_CB_finish_timestamp", StringType(), True), \
        StructField("task_CB_minTemperature", StringType(), True), \
        StructField("task_CB_maxTemperature", StringType(), True), \
        StructField("task_CB_avgTemperature", StringType(), True), \
        StructField("task_CB_minPreasure", StringType(), True), \
        StructField("task_CB_maxPreasure", StringType(), True), \
        StructField("task_CB_avgPreasure", StringType(), True), \
        StructField("task_CC_start_timestamp", StringType(), True), \
        StructField("task_CC_finish_timestamp", StringType(), True), \
        StructField("task_CC_minTemperature", StringType(), True), \
        StructField("task_CC_maxTemperature", StringType(), True), \
        StructField("task_CC_avgTemperature", StringType(), True), \
        StructField("task_CC_minPreasure", StringType(), True), \
        StructField("task_CC_maxPreasure", StringType(), True), \
        StructField("task_CC_avgPreasure", StringType(), True), \
        StructField("task_CD_start_timestamp", StringType(), True), \
        StructField("task_CD_finish_timestamp", StringType(), True), \
        StructField("task_CD_minTemperature", StringType(), True), \
        StructField("task_CD_maxTemperature", StringType(), True), \
        StructField("task_CD_avgTemperature", StringType(), True), \
        StructField("task_CD_minPreasure", StringType(), True), \
        StructField("task_CD_maxPreasure", StringType(), True), \
        StructField("task_CD_avgPreasure", StringType(), True), \
        StructField("task_CE_start_timestamp", StringType(), True), \
        StructField("task_CE_finish_timestamp", StringType(), True), \
        StructField("task_CE_minTemperature", StringType(), True), \
        StructField("task_CE_maxTemperature", StringType(), True), \
        StructField("task_CE_avgTemperature", StringType(), True), \
        StructField("task_CE_minPreasure", StringType(), True), \
        StructField("task_CE_maxPreasure", StringType(), True), \
        StructField("task_CE_avgPreasure", StringType(), True), \
        StructField("task_CF_timestamp", StringType(), True), \
        StructField("task_CF_worker", StringType(), True), \
        StructField("task_CF_order", StringType(), True), \
        StructField("task_D_start_timestamp", StringType(), True), \
        StructField("task_D_finish_timestamp", StringType(), True), \
        StructField("task_D_worker", StringType(), True), \
        StructField("task_D_transport", StringType(), True), \
        StructField("task_D_order", StringType(), True), \
        StructField("task_D_minTemperature", StringType(), True), \
        StructField("task_D_maxTemperature", StringType(), True), \
        StructField("task_D_avgTemperature", StringType(), True), \
        StructField("task_D_minHumidity", StringType(), True), \
        StructField("task_D_maxHumidity", StringType(), True), \
        StructField("task_D_avgHumidity", StringType(), True), \
        StructField("task_EA_timestamp", StringType(), True), \
        StructField("task_EA_worker", StringType(), True), \
        StructField("task_EA_order", StringType(), True), \
        StructField("task_EB_timestamp", StringType(), True), \
        StructField("task_EB_worker", StringType(), True), \
        StructField("task_EB_order", StringType(), True), \
        StructField("task_EB_storage_pallet", StringType(), True), \
        StructField("task_EB_storage_hall", StringType(), True), \
        StructField("task_EB_storage_number", StringType(), True)
        ])

    df = spark.createDataFrame(data=data, schema=schema)
    df.show()
    return df
'''
