# Assemble Pipeline: Understanding User Behavior

In this project, I'm working for a game development company and interested in tracking various user events from their mobile app when they are playing our game online (i.e. `buy a sword`, `join guild`). Each event has metadata characteristic (i.e., sword type, guild name, etc). My goal is to build and pump a complete data pipeline end-to-end, and explain the pipeline in the project report.


## Tasks

- Instrument an API server to log events to Kafka
- Assemble a data pipeline to catch these events: use Spark streaming to filter select event types from Kafka, land them into HDFS/parquet to make them available for analysis using Presto. 
- Use Apache Bench to generate test data for my pipeline.
- Query Batch Data with Presto
- Produce an analytics report where I provide a description of the pipeline and some basic analysis of the events. 


## Project files:

- **project_report.ipynb** is the final report of the project with data pipeline explanation 
- **docker-compose.yml** inlcude all docker containers required for running this project
- **game_api.py** Flask app for building an API server for the game and sending event logs (streaming data) to Kafka 
- **generate_data.sh** Generate GET and POST requests/ streaming events using Apache Bench
- **write_stream.py** Consume the messages from Kafka, filter events, transform and land the data in Hadoop (HDFS)
