# ETL Data Pipeline: Tracking User Activity
--------

In this project, I will use a nested json data extracted from an ed tech firm database, who provides service that delivers various assessments to different customers in Tech. I will explain the detailed steps on how to extract, transform and load (ETL) the data through the pipeline and prepare the data ready for data scientists to run queries on.

The main goal of this project is explaining the pipeline as demonstrated in the jupyter notebook report.

## Tasks

Prepare the infrastructure to land the data in the form and structure it needs to be in order to run queries. I will perform the following tasks:

- Publish and consume messages with Kafka, the message sent is the nested json data.
- Use Spark to transform the messages so that they can be landed in Hadoop (HDFS)
- Run queries, brief analysis of the transformed data  
