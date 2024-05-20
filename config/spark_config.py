SPARK_APP_NAME = "AdvertiseX Data Processing"
SPARK_MASTER = "local[*]"
SPARK_HUDI_OPTIONS = {
    'hoodie.table.name': 'ad_events',
    'hoodie.datasource.write.recordkey.field': 'user_id',
    'hoodie.datasource.write.partitionpath.field': 'website',
    'hoodie.datasource.write.table.name': 'ad_events',
    'hoodie.datasource.write.operation': 'upsert',
    'hoodie.datasource.write.precombine.field': 'timestamp',
    'hoodie.upsert.shuffle.parallelism': 2,
    'hoodie.insert.shuffle.parallelism': 2
}
