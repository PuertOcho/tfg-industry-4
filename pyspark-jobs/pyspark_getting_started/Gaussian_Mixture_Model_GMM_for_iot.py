from math import sqrt

from pyspark.sql import SparkSession
import os
import config
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.clustering import GaussianMixture
from pyspark.ml.evaluation import ClusteringEvaluator
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

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



    maxKclusters = 8

    cost = np.zeros(maxKclusters)

    for k in range(2, maxKclusters):

        gmm = GaussianMixture().setK(k).setSeed(538009335)
        model = gmm.fit(scaledDataDF)

        print("Gaussians shown as a DataFrame: ")
        model.gaussiansDF.show(truncate=False)

        # Make predictions
        predictions = model.transform(scaledDataDF)

        # Evaluate clustering by computing Silhouette score
        evaluator = ClusteringEvaluator()

        silhouette = evaluator.evaluate(predictions)
        print("Silhouette with squared euclidean distance = " + str(silhouette))


        cost[k] = silhouette


    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.plot(range(2, maxKclusters), cost[2:maxKclusters])
    ax.set_xlabel('k')
    ax.set_ylabel('silhouette')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()
