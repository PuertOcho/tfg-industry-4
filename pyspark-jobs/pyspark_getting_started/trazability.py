import json

from pyspark.sql import SparkSession
import os
import config

from pyspark.sql.functions import pandas_udf, PandasUDFType
import pyspark.sql.functions as f
from pyspark.sql.functions import explode
import pandas as pd
from pyspark.sql.functions import min


def apply(spark: SparkSession, ID ):
    # inferSchema = true, so that it can successfully infer data types (otherwise, it will set all columns as strings)
    # https://stackoverflow.com/questions/29725612/spark-csv-data-source-infer-data-types
# array_contains(df("languages"),"Java")

    #ID = 'PH27A59CC2'
    ds = spark.read.option("header", "true").option("inferSchema", "true").json(
        os.path.join(config.ROOT_DIR, 'data/sensors_complete_data_json/data.json'))
    ds.printSchema()
    # ds.show(n= 112)

    task_CB_CC_CD_CE = ds.filter(f.col('id') == ID)
    task_CB_CC_CD_CE.show(n=50)

    task_AA_AB_CA = ds.filter(f.array_contains(ds.milkTanks, ID)) #AA AB CA
    #task_AA_AB_CA.show()

    order_t1 = task_AA_AB_CA.filter(task_AA_AB_CA.task == 'AB').select("order").first()[0]
    task_AB_B_CA = ds.filter(ds.order == order_t1) #AB B CA
    #task_AB_B_CA.show(n=50)

    task_CF_EA = ds.filter(f.array_contains(ds.pallets, ID)) #CF EA
    #task_CF_EA.show()

    order_t2 = task_CF_EA.filter(task_CF_EA.task == 'EA').select("order").first()[0]
    task_CF_D_EA_EB = ds.filter( ds.order == order_t2) #CF D EA EB
    task_CF_D_EA_EB.show()


    # Etapa proveedor
    task_AA = task_AA_AB_CA.filter(task_AA_AB_CA.task == 'AA').select('timestamp', 'supplier', 'worker').collect()[0]
    task_AB = task_AA_AB_CA.filter(task_AA_AB_CA.task == 'AB').select('timestamp', 'supplier', 'worker', 'order').collect()[0]

    supplier_stage_json = json.dumps({
        "task_AA":{'timestamp':task_AA[0], 'supplier':task_AA[1],'worker':task_AA[2]},
        "task_AB":{'timestamp':task_AB[0], 'supplier':task_AB[1],'worker':task_AB[2], 'order':task_AB[3]}
    }, indent=3)

    print(supplier_stage_json)


    # Etapa transporte 1
    task_B = task_AB_B_CA.filter(task_AB_B_CA.task == 'B').select('worker', 'transport', 'order', 'temperature', 'humidity').collect()[0]
    task_B_metrics = task_AB_B_CA.filter(task_AB_B_CA.task == 'B').agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("humidity").alias("minHumidity"),
        f.max("humidity").alias("maxHumidity"),
        f.avg("humidity").alias("avgHumidity"),
        f.min("timestamp").alias("start_timestamp"),
        f.max("timestamp").alias("finish_timestamp")).collect()[0]

    transport_1_stage_json = json.dumps({
        "task_B": {'start_timestamp': task_B_metrics.start_timestamp, 'finish_timestamp':task_B_metrics.finish_timestamp,
                  'worker': task_B.worker, 'transport': task_B.transport, 'order': task_B.order,
                  'minTemperature': task_B_metrics.minTemperature, 'maxTemperature': task_B_metrics.maxTemperature, 'avgTemperature':task_B_metrics.avgTemperature,
                  'minHumidity': task_B_metrics.minHumidity, 'maxHumidity': task_B_metrics.maxHumidity, 'avgHumidity': task_B_metrics.avgHumidity}
    }, indent=3)

    print(transport_1_stage_json)


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
    print(task_CF)

    factory_stage_json = json.dumps({
        "task_CA": {'timestamp': task_CA.timestamp,
                    'worker': task_CA.worker,
                    'order': task_CA.order},
        "task_CB": {'start_timestamp': task_CB_metrics.start_timestamp,
                   'finish_timestamp': task_CB_metrics.finish_timestamp,
                   'minTemperature': task_CB_metrics.minTemperature,
                   'maxTemperature': task_CB_metrics.maxTemperature,
                   'avgTemperature': task_CB_metrics.avgTemperature,
                   'minPreasure': task_CB_metrics.minPreasure,
                   'maxPreasure': task_CB_metrics.maxPreasure,
                   'avgPreasure': task_CB_metrics.avgPreasure},
        "task_CC": {'start_timestamp': task_CC_metrics.start_timestamp,
                   'finish_timestamp': task_CC_metrics.finish_timestamp,
                   'minTemperature': task_CC_metrics.minTemperature,
                   'maxTemperature': task_CC_metrics.maxTemperature,
                   'avgTemperature': task_CC_metrics.avgTemperature,
                   'minPreasure': task_CC_metrics.minPreasure,
                   'maxPreasure': task_CC_metrics.maxPreasure,
                   'avgPreasure': task_CC_metrics.avgPreasure},
        "task_CD": {'start_timestamp': task_CD_metrics.start_timestamp,
                   'finish_timestamp': task_CD_metrics.finish_timestamp,
                   'minTemperature': task_CD_metrics.minTemperature,
                   'maxTemperature': task_CD_metrics.maxTemperature,
                   'avgTemperature': task_CD_metrics.avgTemperature,
                   'minPreasure': task_CD_metrics.minPreasure,
                   'maxPreasure': task_CD_metrics.maxPreasure,
                   'avgPreasure': task_CD_metrics.avgPreasure},
        "task_CE": {'start_timestamp': task_CE_metrics.start_timestamp,
                   'finish_timestamp': task_CE_metrics.finish_timestamp,
                   'minTemperature': task_CE_metrics.minTemperature,
                   'maxTemperature': task_CE_metrics.maxTemperature,
                   'avgTemperature': task_CE_metrics.avgTemperature,
                   'minPreasure': task_CE_metrics.minPreasure,
                   'maxPreasure': task_CE_metrics.maxPreasure,
                   'avgPreasure': task_CE_metrics.avgPreasure},
        "task_CF": {'timestamp': task_CF.timestamp,
                    'worker': task_CF.worker,
                    'order': task_CF.order}
    }, indent=3)

    print(factory_stage_json)


    # Etapa transporte 2
    task_D = task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'D').select('worker', 'transport', 'order', 'temperature', 'humidity').collect()[0]
    task_D_metrics = task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'D').agg(
        f.min("temperature").alias("minTemperature"),
        f.max("temperature").alias("maxTemperature"),
        f.avg("temperature").alias("avgTemperature"),
        f.min("humidity").alias("minHumidity"),
        f.max("humidity").alias("maxHumidity"),
        f.avg("humidity").alias("avgHumidity"),
        f.min("timestamp").alias("start_timestamp"),
        f.max("timestamp").alias("finish_timestamp")).collect()[0]

    transport_2_stage_json = json.dumps({
        "task_D": {'start_timestamp': task_D_metrics.start_timestamp,
                   'finish_timestamp':task_D_metrics.finish_timestamp,
                   'worker': task_D.worker,
                   'transport': task_D.transport,
                   'order': task_D.order,
                   'minTemperature': task_D_metrics.minTemperature,
                   'maxTemperature': task_D_metrics.maxTemperature,
                   'avgTemperature':task_D_metrics.avgTemperature,
                   'minHumidity': task_D_metrics.minHumidity,
                   'maxHumidity': task_D_metrics.maxHumidity,
                   'avgHumidity': task_D_metrics.avgHumidity}
    }, indent=3)

    print(transport_2_stage_json)


    # Etapa almacen

    task_EA = task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'EA').select('timestamp', 'worker', 'order').collect()[0]
    task_EB = task_CF_D_EA_EB.filter(task_AB_B_CA.task == 'EB').select('timestamp', 'worker', 'order', 'storage').collect()[0]

    store_stage_json = json.dumps({
        "task_EA": {'timestamp': task_EA.timestamp,
                   'worker':task_EA.worker,
                   'order': task_EA.order},
        "task_EB": {'timestamp': task_EB.timestamp,
                   'worker': task_EB.worker,
                   'order': task_EB.order,
                   'storage': task_EB.storage}
    }, indent=3)

    print(store_stage_json)


    res_json = json.dumps({
        'id': ID,
        'supplier_stage': supplier_stage_json,
        'transport_1_stage': transport_1_stage_json,
        'factory_stage': factory_stage_json,
        'transport_2_stage': transport_2_stage_json,
        'store_stage': store_stage_json
    })

    print(res_json)