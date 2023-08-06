from pyspark.sql import SparkSession
import os
import config
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import GBTClassifier

def apply(spark : SparkSession):

    ds = spark.read.option("header", "true").option("inferSchema", "true").json(
        os.path.join(config.ROOT_DIR, 'data/data_for_ML/data.json')).select(['id', 'goodness',
                                          'minTemperature_CB', 'maxTemperature_CB', 'avgTemperature_CB',
                                          'minPreasure_CB', 'maxPreasure_CB', 'avgPreasure_CB',
                                          'minTemperature_CC', 'maxTemperature_CC', 'avgTemperature_CC',
                                          'minPreasure_CC', 'maxPreasure_CC', 'avgPreasure_CC',
                                          'minTemperature_CD', 'maxTemperature_CD', 'avgTemperature_CD',
                                          'minPreasure_CD', 'maxPreasure_CD', 'avgPreasure_CD',
                                          'minTemperature_CE', 'maxTemperature_CE', 'avgTemperature_CE',
                                          'minPreasure_CE', 'maxPreasure_CE', 'avgPreasure_CE',
                                          'minTemperature_tranport1', 'maxTemperature_tranport1',
                                          'avgTemperature_tranport1',
                                          'minHumidity_tranport1', 'maxHumidity_tranport1', 'avgHumidity_tranport1',
                                          'minTemperature_tranport2', 'maxTemperature_tranport2',
                                          'avgTemperature_tranport2',
                                          'minHumidity_tranport2', 'maxHumidity_tranport2', 'avgHumidity_tranport2'])


    labelCol = "goodness"
    trainDF, testDF = ds.randomSplit([.9, .1], seed=43)


    inputCols = trainDF.columns[2: len(trainDF.columns)]

    vecAssembler = VectorAssembler( inputCols=inputCols, outputCol="features").setHandleInvalid("skip")
    vecTrainDF = vecAssembler.transform(trainDF)
    vecTrainDF.select("features").show(10, False)

    stdScaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=False)

    scalerModel = stdScaler.fit(vecTrainDF)

    scaledDataDF = scalerModel.transform(vecTrainDF)
    scaledDataDF.select("scaledFeatures").show(10, False)


    # Gradient-Boosted Tree
    gbt = GBTClassifier(labelCol=labelCol, featuresCol="scaledFeatures", maxIter=10)


    #Pipeline
    pipeline_gbt = Pipeline(stages=[vecAssembler, stdScaler, gbt])
    pipelineModel_gbt = pipeline_gbt.fit(trainDF)

    predDF_gbt = pipelineModel_gbt.transform(testDF)

    # Evaluator
    evaluator = MulticlassClassificationEvaluator( labelCol=labelCol, predictionCol="prediction", metricName="accuracy")

    gbt_accuracy = evaluator.evaluate(predDF_gbt)
    print("Accuracy of Gradient-Boosted Tree is = %g" % (gbt_accuracy))
    print("Error of Gradient-Boosted Tree is = %g " % (1.0 - gbt_accuracy))
