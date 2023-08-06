import re

regex = re.compile('[^a-zA-Z]')

def apply(sc, data):
    rdd = sc\
        .parallelize(data.split())\
        .map(lambda word: (regex.sub('', word.lower()), 1))\
        .reduceByKey(lambda x, y: x+y)\
        .sortBy(lambda x: -x[-1])
    result = rdd.collect()
    #[print(x) for x in result]
    sc.stop()
