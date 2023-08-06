from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import lit
import pyspark.sql.functions as f
import sys
from pymongo import MongoClient
import glob, os
import config
import time
from pyspark_getting_started import word_count, read_mongodb, mongodb_to_csv, groupby_pandas_udf, groupby_arrays, \
    mongodb_to_json, trazability, groupby_input_mllib, generate_data_ML, logisticRegression_for_iot, \
    linearSVC_for_iot, randomForest_for_iot, OneVsRest_for_iot, decisionTree_for_iot, naiveBayes_for_iot, \
    FMClassifier_for_iot, GBTClassifier_for_iot, MultilayerPerceptronClassifier_for_iot, k_means_for_iot, \
    Gaussian_Mixture_Model_GMM_for_iot, \
    Latent_Dirichlet_allocation_LDA_for_iot, Bisecting_k_means_for_iot, trazability2, spark_to_mongo

ACTION = str(sys.argv[1])

example_data = \
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi mollis, velit sit amet pretium sagittis, erat mauris egestas nisl, eget facilisis lectus est et magna. Proin interdum libero a libero pretium vestibulum. Maecenas placerat, lacus lacinia tincidunt mattis, orci sapien consequat tortor, in volutpat neque ligula maximus nibh. Nullam tempor orci dolor, a condimentum massa porttitor a. Donec id ipsum et orci mollis condimentum. In feugiat mollis justo ut tincidunt. Suspendisse pharetra lacus feugiat mollis aliquet. Phasellus pretium egestas sagittis. Morbi tempus risus nec justo blandit, venenatis maximus felis interdum. Etiam ultrices vel dui vel vehicula. Quisque sit amet eros vehicula, eleifend tortor ac, elementum velit. In hac habitasse platea dictumst. Vestibulum faucibus suscipit erat, at sollicitudin metus consequat sit amet.
    Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur et feugiat erat, in rhoncus ante. Integer a magna et lectus lobortis vestibulum eget a mauris. Sed varius ante vitae diam tristique rutrum. Donec quis mauris eu eros faucibus accumsan quis a magna. Cras at libero vitae mi pellentesque mollis. Aliquam at diam metus. Suspendisse potenti. Mauris consequat eget neque ullamcorper molestie. Nam mollis erat quam, sed pellentesque dolor lacinia eu. Nam eget mauris in nisl aliquam efficitur. In pretium diam mauris, eget elementum justo ultrices at.
    """


def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename,
                  os.path.join(dir, titlePattern + ext))


def get_spark_context():
    conf = SparkConf().setAppName('pyspark_getting_started') \
        .setMaster("local[*]")
    sc = SparkContext(conf=conf)
    return sc


def get_spark_session(db_in, db_out):
    spark_session = SparkSession \
        .builder \
        .appName("pyspark_getting_started") \
        .master("local[*]") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.mongodb.input.uri", db_in) \
        .config("spark.mongodb.output.uri", db_out) \
        .config("spark.driver.extraJavaOptions", "-Dio.netty.tryReflectionSetAccessible=true") \
        .config("spark.executor.extraJavaOptions", "-Dio.netty.tryReflectionSetAccessible=true") \
        .getOrCreate()
    return spark_session

# ML - Classification
# k_means_for_iot.apply(get_spark_session()) #
# Gaussian_Mixture_Model_GMM_for_iot.apply(get_spark_session())
# Latent_Dirichlet_allocation_LDA_for_iot.apply(get_spark_session())
# Bisecting_k_means_for_iot.apply(get_spark_session())

# Trazability
# trazability.apply( get_spark_session(), "0VAFWB0S") # 2CYFULXO, 5Z888JZ7, P7GLFJSZ, Y3CW4Z8C
# aux = trazability2.apply( get_spark_session(), "PH27A59CC2") # 2CYFULXO, 5Z888JZ7, P7GLFJSZ, Y3CW4Z8C, PH27A59CC2

# Spark to MongoDB
# spark_to_mongo.apply()

if __name__ == '__main__':
    initial_timestamp = int(time.time())

    if ACTION == 'initest':
        word_count.apply(get_spark_context(), example_data)

    if ACTION == 'prepare':
        correctDataPath = 'data/train/data_correct'
        correct_mongodb_uri = 'mongodb+srv://admin:admin@cluster0.s76am.mongodb.net/TFG.TFGCollectionCorrecto'

        mongodb_to_json.apply(get_spark_session(correct_mongodb_uri, correct_mongodb_uri), correctDataPath)
        rename((config.ROOT_DIR + '/' + correctDataPath), r'*.json', 'data')

        errorDataPath = 'data/train/data_error'
        error_mongodb_uri = 'mongodb+srv://admin:admin@cluster0.s76am.mongodb.net/TFG.TFGCollectionFallosTarea'

        mongodb_to_json.apply(get_spark_session(error_mongodb_uri, error_mongodb_uri), errorDataPath)
        rename((config.ROOT_DIR + '/' + errorDataPath), r'*.json', 'data')

        pathML = 'data/train/full_data'
        generate_data_ML.apply(get_spark_session(config.mongo_uri_in_default, config.mongo_uri_out_default), pathML)
        rename((config.ROOT_DIR + '/' + pathML), r'*.json', 'data')

    if ACTION == 'train':
        df_complete = get_spark_session(config.mongo_uri_in_default, config.mongo_uri_out_default) \
            .read.option("header", "true").option("inferSchema", "true") \
            .json(os.path.join(config.ROOT_DIR, 'data/train/full_data/data.json')) \
            .select(config.transport_factory_fields)

        df_transport = df_complete.filter((df_complete.task == "B") | (df_complete.task == "D")).select(
            config.transport_fields)
        df_factory_CB = df_complete.filter("task == 'CB'").select(config.factory_fields)
        df_factory_CC = df_complete.filter("task == 'CC'").select(config.factory_fields)
        df_factory_CD = df_complete.filter("task == 'CD'").select(config.factory_fields)
        df_factory_CE = df_complete.filter("task == 'CE'").select(config.factory_fields)

        MultilayerPerceptronClassifier_for_iot.apply(df_transport, "B_D")
        MultilayerPerceptronClassifier_for_iot.apply(df_factory_CB, "CB")
        MultilayerPerceptronClassifier_for_iot.apply(df_factory_CC, "CC")
        MultilayerPerceptronClassifier_for_iot.apply(df_factory_CD, "CD")
        MultilayerPerceptronClassifier_for_iot.apply(df_factory_CE, "CE")

        # FMClassifier_for_iot.apply(get_spark_session()) # 0.769366 / 0.230634
        # logisticRegression_for_iot.apply(get_spark_session()) # 0.78443 / 0.21557
        # linearSVC_for_iot.apply(get_spark_session()) # 0.72007 / 0.27993
        # naiveBayes_for_iot.apply(get_spark_session()) # 0.994718 / 0.00528169
        # decisionTree_for_iot.apply(get_spark_session()) # 0.867958 / 0.132042
        # randomForest_for_iot.apply(get_spark_session()) #  0.880282 / 0.119718
        # GBTClassifier_for_iot.apply(get_spark_session()) # 0.984155 / 0.0158451

    if ACTION == 'predict':
        spark_session = get_spark_session(config.mongo_to_process_uri, config.mongo_processed_uri)

        # cargar modelos
        pipelineModel_mpc_B_D = PipelineModel.load(
            os.path.join(config.ROOT_DIR, 'data/models/model_B_D/multilayerPerceptronClassifier'))
        pipelineModel_mpc_CB = PipelineModel.load(
            os.path.join(config.ROOT_DIR, 'data/models/model_CB/multilayerPerceptronClassifier'))
        pipelineModel_mpc_CC = PipelineModel.load(
            os.path.join(config.ROOT_DIR, 'data/models/model_CC/multilayerPerceptronClassifier'))
        pipelineModel_mpc_CD = PipelineModel.load(
            os.path.join(config.ROOT_DIR, 'data/models/model_CD/multilayerPerceptronClassifier'))
        pipelineModel_mpc_CE = PipelineModel.load(
            os.path.join(config.ROOT_DIR, 'data/models/model_CE/multilayerPerceptronClassifier'))
        #print('------------------------ modelos cargados ------------------------')

        # coger datos para procesar
        df_all = read_mongodb.apply(spark_session)

        # Procesar los resultados y guardamos los datos en carpetas temporales
        temp_transport_predicted_path = 'data/temp/transport_predicted_data'
        df_input_model = groupby_input_mllib.apply(df_all).withColumn('goodness', lit(1))
        df_transports = pipelineModel_mpc_B_D.transform(
            df_input_model.filter((df_input_model.task == "B") | (df_input_model.task == "D")).select(
                config.transport_fields)).drop("goodness").withColumn("stage", lit("Prediction"))
        df_transports.coalesce(1).write.format('json').save(
            temp_transport_predicted_path, mode="overwrite")
        rename((config.ROOT_DIR + '/' + temp_transport_predicted_path), r'*.json', 'data')

        temp_factory_predicted_path = 'data/temp/factory_predicted_data'
        CB_predictions = pipelineModel_mpc_CB.transform(df_input_model.filter((df_input_model.task == "CB"))
                                                        .select(config.factory_fields)).drop("goodness")
        CC_predictions = pipelineModel_mpc_CC.transform(df_input_model.filter((df_input_model.task == "CC")).select(
            config.factory_fields)).drop("goodness")
        CD_predictions = pipelineModel_mpc_CD.transform(df_input_model.filter((df_input_model.task == "CD")).select(
            config.factory_fields)).drop("goodness")
        CE_predictions = pipelineModel_mpc_CE.transform(df_input_model.filter((df_input_model.task == "CE")).select(
            config.factory_fields)).drop("goodness")
        df_factory = CB_predictions.union(CC_predictions).union(CD_predictions).union(CE_predictions) \
            .withColumn("stage", lit("Prediction"))
        df_factory.coalesce(1).write.format('json').save(temp_factory_predicted_path, mode="overwrite")
        rename((config.ROOT_DIR + '/' + temp_factory_predicted_path), r'*.json', 'data')

        df_all.show(n=50)
        df_factory.show(n=50)
        df_transports.show(n=50)

        df_all.write.format("mongo") \
            .option('uri', config.mongo_processed_uri + config.sufix_secuity_mongo_config).option('database', 'TFG') \
            .option('collection', 'TFGCollectionProcessed').option('collection', 'TFGCollectionProcessed') \
            .mode("append").save()

        df_transports.drop("features", "scaledFeatures", "rawPrediction", "probability").write.format("mongo") \
            .option('uri', config.mongo_processed_uri + config.sufix_secuity_mongo_config).option('database', 'TFG') \
            .option('collection', 'TFGCollectionProcessed').option('collection', 'TFGCollectionProcessed') \
            .mode("append").save()

        df_factory.drop("features", "scaledFeatures", "rawPrediction", "probability").write.format("mongo") \
            .option('uri', config.mongo_processed_uri + config.sufix_secuity_mongo_config).option('database', 'TFG') \
            .option('collection', 'TFGCollectionProcessed').option('collection', 'TFGCollectionProcessed') \
            .mode("append").save()

        spark_session.stop()

        # Borramos los datos ya procesados
        mongo_client = MongoClient(config.mongo_uri)
        collectionToProcess = mongo_client["TFG"][config.collectionToProcess]
        x = collectionToProcess.delete_many({})
        print(x.deleted_count, " documents deleted of collectionToProcess.")
        mongo_client.close()

    if ACTION == 'clear':
        # borrar contenido db entrada
        mongo_client = MongoClient(config.mongo_to_process_uri)
        collection = mongo_client[config.database][config.collectionToProcess] # TO PROCESS
        #collection = mongo_client[config.database][config.collectionProcessed]  # PROCESSED
        x = collection.delete_many({})
        print(x.deleted_count, " documents deleted.")

    if ACTION == 'clearAll':
        # borrar contenido db entrada
        mongo_client = MongoClient(config.mongo_to_process_uri)
        collectionToProcess = mongo_client[config.database][config.collectionToProcess]
        collectionProcessed = mongo_client[config.database][config.collectionProcessed]
        x = collectionToProcess.delete_many({})
        y = collectionProcessed.delete_many({})
        print(x.deleted_count, " documents collectionToProcess deleted.")
        print(y.deleted_count, " documents collectionProcessed deleted.")

    processingTime = (int(time.time()) - int(initial_timestamp))
    timestamp = int(time.time())
    print("{action:" + str(ACTION) + ",timestamp:" + str(timestamp) + ",processingTime:" + str(processingTime) + "}")
