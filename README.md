# AdvertiseX Data Pipeline

This project is a data engineering solution for AdvertiseX, designed to handle data ingestion, processing, storage, and monitoring of ad impression, click, and bid request data.

## File Structure

- `ingestion/`: Contains Kafka producer and consumer scripts.
- `processing/`: Contains Spark processing and Hudi writing scripts.
- `config/`: Contains configuration files.
- `monitoring/`: Contains Prometheus and Grafana configuration files.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

## Setup

1. Start Kafka and create necessary topics.
2. Run the Kafka producer.
3. Run the Kafka consumer.
4. Start Spark processing and Hudi writing jobs.
5. Set up Prometheus and Grafana for monitoring.

## Execution

1. Start Kafka and create topics:
   ```sh
   bin/kafka-topics.sh --create --topic ad_impressions --bootstrap-server localhost:9092
   bin/kafka-topics.sh --create --topic ad_clicks --bootstrap-server localhost:9092
   bin/kafka-topics.sh --create --topic bid_requests --bootstrap-server localhost:9092

2. Run Kafka producer:
>>> python ingestion/kafka_producer.py

3. Run Kafka consumer:
>>> python ingestion/kafka_consumer.py

4. Start Spark processing jobs:
>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.hudi:hudi-spark-bundle_2.12:0.9.0 processing/spark_processor.py
>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org

5. Configure and start Prometheus and Grafana.

## Monitoring
Prometheus will scrape metrics from Kafka and Spark, and Grafana will visualize them. Import the provided Grafana dashboard JSON to set up the visualizations.