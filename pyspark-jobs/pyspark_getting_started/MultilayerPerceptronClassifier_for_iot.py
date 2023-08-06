import string

from pyspark.sql import SparkSession
import os
import config
from pyspark.sql.dataframe import DataFrame
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import MultilayerPerceptronClassifier

# Multilayer Perceptron Classifier
def apply(df: DataFrame, task: string):

    labelCol = "goodness"
    trainDF, testDF = df.randomSplit([.9, .1], seed=43)

    inputCols = trainDF.columns[2: len(trainDF.columns)]

    vecAssembler = VectorAssembler(inputCols=inputCols, outputCol="features").setHandleInvalid("skip")
    vecTrainDF = vecAssembler.transform(trainDF)
    # vecTrainDF.select("features").show(10, False)

    stdScaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=False)
    scalerModel = stdScaler.fit(vecTrainDF)
    scaledDataDF = scalerModel.transform(vecTrainDF)
    # scaledDataDF.select("scaledFeatures").show(10, False)

    # Multilayer Perceptron Classifier
    layers = [len(trainDF.columns) - 2, 72, 144, 72, 2]
    mlp = MultilayerPerceptronClassifier(labelCol=labelCol, featuresCol="scaledFeatures", maxIter=100, layers=layers,
                                         blockSize=128, seed=1234)

    # Pipeline
    pipeline_mlp = Pipeline(stages=[vecAssembler, stdScaler, mlp])
    pipelineModel_mlp = pipeline_mlp.fit(trainDF)

    # Prediction test
    predDF_mlp = pipelineModel_mlp.transform(testDF)
    onlyPredictionOne = predDF_mlp.filter("prediction == 1")
    #print(task + " : " + str(onlyPredictionOne.count()))
    onlyPredictionOne.show(n=10)

    # show data
    print(task + " : " + str(df.count()))
    print("trainDF : " + str(trainDF.count()))
    print("testDF : " + str(testDF.count()))

    # save Data
    modelPath = os.path.join(config.ROOT_DIR,
                             'data/models/model_' + task + '/multilayerPerceptronClassifier')
    #pipelineModel_mlp.write().overwrite().save(modelPath)

    # Evaluator
    evaluator = MulticlassClassificationEvaluator(labelCol=labelCol, predictionCol="prediction", metricName="accuracy")
    mlp_accuracy = evaluator.evaluate(predDF_mlp)

    print("Accuracy of MLP Classifier is = %g" % (mlp_accuracy))
    print("Error of MLP Classifier is = %g " % (1.0 - mlp_accuracy))
