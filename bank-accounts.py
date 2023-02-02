import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructField, StructType, StringType, IntegerType
from pyspark.sql.functions import col, udf

# Create a Spark Session
spark = SparkSession\
    .builder\
    .appName("Bank Account location")\
    .getOrCreate()

# Read Bank account data created with datagen
df = spark.read.parquet("/user/datagen/hdfs/banking/bank_account/")
df.printSchema()
df.show()

# Define a google maps function.
from IPython.display import IFrame
from IPython.core.display import display
def gmaps(query):
  url = "https://maps.google.com/maps?q={0}&output=embed".format(query)
  display(IFrame(url, '700px', '450px'))

# Group and count peeople per city
df_grouped_by_city = df.groupBy('city_of_residence').count()
data_joined = df_grouped_by_city.join(df, ['city_of_residence']).dropDuplicates(['city_of_residence']).sort(col("count").desc())

# Get ten cities with most accounts
ten_rows = data_joined.take(10)

# Print on a map
for idx, i in enumerate(ten_rows):
  print(str(idx+1) + "/10 of the most customer's cities are: " + i.__getitem__('city_of_residence'))
  gmaps(i.__getitem__('city_of_residence')+", USA")
