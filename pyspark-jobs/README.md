# Pyspark-getting-started

Just a getting-started project :)

Template for `config.py` (must be placed in the root directory):

```python
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

mongo_uri = ""
```

For Spark (java or pyskar) to work in Windows: https://phoenixnap.com/kb/install-spark-on-windows-10

- Download Spark
- Unzip Spark in `C:\`
- Download winutils.exe from https://github.com/cdarlint/winutils 
- Create directory `/hadoop/bin` in `C:\` and paste there `winutils.exe`
- Create environment variable `SPARK_HOME` pointing at the Spark's directory
- Add `%SPARK_HOME%\bin` to the Path
- Create environment variable `HADOOP_HOME` pointing at `C:\hadoop`
- Add `%HADOOP_HOME%\bin` to the Path

Deploying pyspark on a cluster: https://towardsdatascience.com/successful-spark-submits-for-python-projects-53012ca7405a
