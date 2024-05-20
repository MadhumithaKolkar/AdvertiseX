from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, split
import pyspark.sql.functions as F

# Spark configuration
spark = SparkSession.builder \
    .appName("AdvertiseX Hudi Writer") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.hudi.write.lock.provider", "org.apache.hudi.common.lock.FileSystemBasedLockProvider") \
    .getOrCreate()

# Define schema for ad impressions
impression_schema = "ad_creative_id INT, user_id INT, timestamp LONG, website STRING"

# Load ad impressions data from Kafka
impressions_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ad_impressions") \
    .load() \
    .selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), impression_schema).alias("data")) \
    .select("data.*")

# Define schema for ad clicks
clicks_schema = "timestamp LONG, user_id INT, ad_campaign_id INT, conversion_type STRING"

# Load ad clicks data from Kafka
clicks_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ad_clicks") \
    .load() \
    .selectExpr("CAST(value AS STRING) as csv") \
    .selectExpr("split(csv, ',') as csv") \
    .select(
        col("csv").getItem(0).cast("long").alias("timestamp"),
        col("csv").getItem(1).cast("int").alias("user_id"),
        col("csv").getItem(2).cast("int").alias("ad_campaign_id"),
        col("csv").getItem(3).alias("conversion_type")
    )

# Join impressions and clicks data on user_id
joined_df = impressions_df.join(clicks_df, "user_id")

# Write the joined dataframe to Hudi
hudi_options = {
    'hoodie.table.name': 'ad_events',
    'hoodie.datasource.write.recordkey.field': 'user_id',
    'hoodie.datasource.write.partitionpath.field': 'website',
    'hoodie.datasource.write.table.name': 'ad_events',
    'hoodie.datasource.write.operation': 'upsert',
    'hoodie.datasource.write.precombine.field': 'timestamp',
    'hoodie.upsert.shuffle.parallelism': 2,
    'hoodie.insert.shuffle.parallelism': 2
}

query = joined_df \
    .writeStream \
    .format("hudi") \
    .options(**hudi_options) \
    .option("checkpointLocation", "s3://your-bucket/checkpoints") \
    .start("s3://your-bucket/hudi/ad_events")

query.awaitTermination()

