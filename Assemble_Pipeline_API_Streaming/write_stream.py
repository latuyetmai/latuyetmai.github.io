#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

def event_schema():
    """
    root
    |-- event_type: string (nullable = true)
    |-- gold_count: string (nullable = true)
    |-- description: string (nullable = true)
    |-- value: string (nullable = true)
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)

    """
    return StructType([
        StructField("event_type", StringType(), True),
        StructField("gold_count", StringType(), True),
        StructField("description", StringType(), True),
        StructField("value", StringType(), True),
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True)])


@udf('boolean')
def is_sword_purchase(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase_sword':
        return True
    return False

@udf('boolean')
def is_guild_join(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'join_guild':
        return True
    return False

@udf('boolean')
def is_gold_earn(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'earn_gold':
        return True
    return False

@udf('boolean')
def is_potion_purchase(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase_potion':
        return True
    return False

def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()

    # Filter purchase_sword event
    sword_purchases = raw_events \
        .filter(is_sword_purchase(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                          event_schema()).alias('json'),
                raw_events.timestamp.cast('string'),
                raw_events.value.cast('string').alias('raw_event')) \
        .select('json.*', 'timestamp', 'raw_event')
       
    sink = sword_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_sword_purchases") \
        .option("path", "/tmp/sword_purchases") \
        .trigger(processingTime="120 seconds") \
        .start()

    # filter join_guild event
    guild_joins = raw_events \
        .filter(is_guild_join(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                          event_schema()).alias('json'),
                raw_events.timestamp.cast('string'),
                raw_events.value.cast('string').alias('raw_event')) \
        .select('json.*', 'timestamp', 'raw_event')

    sink2 = guild_joins \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_guild_joins") \
        .option("path", "/tmp/guild_joins") \
        .trigger(processingTime="120 seconds") \
        .start()

    # filter earn_gold event
    gold_earns = raw_events \
        .filter(is_gold_earn(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                          event_schema()).alias('json'),
                raw_events.timestamp.cast('string'),
                raw_events.value.cast('string').alias('raw_event')) \
        .select('json.*', 'timestamp', 'raw_event')

    sink3 = gold_earns \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_gold_earns") \
        .option("path", "/tmp/gold_earns") \
        .trigger(processingTime="120 seconds") \
        .start()

    # filter purchase_potion event
    potion_purchases = raw_events \
        .filter(is_potion_purchase(raw_events.value.cast('string'))) \
        .select(from_json(raw_events.value.cast('string'),
                          event_schema()).alias('json'),
                raw_events.timestamp.cast('string'),
                raw_events.value.cast('string').alias('raw_event')) \
        .select('json.*', 'timestamp', 'raw_event')

    sink4 = potion_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_potion_purchases") \
        .option("path", "/tmp/potion_purchases") \
        .trigger(processingTime="120 seconds") \
        .start()
    
    # All events
    all_events = raw_events \
        .select(from_json(raw_events.value.cast('string'),
                          event_schema()).alias('json'),
                raw_events.timestamp.cast('string'),
                raw_events.value.cast('string').alias('raw_event')) \
        .select('json.*', 'timestamp', 'raw_event')

    sink5 = all_events \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_all_events") \
        .option("path", "/tmp/all_events") \
        .trigger(processingTime="120 seconds") \
        .start()
    
    spark.streams.awaitAnyTermination()

    
if __name__ == "__main__":
    main()
