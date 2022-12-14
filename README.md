# miband Elastic Importer

This project written in Python has the function of importing monitoring data captured by MiBand into indexes in ES.
It is currently possible to import data: Activity, Heart Rate, Sleep and Sport.

## Technologies

* Python
* Elasticsearch

## Pre-requisites

### Run docker-compose

````
docker-compose up -d
````

### Mapping

All mappings are located in the project's "mappings" folder.

Execute the command below so that the indexes are created:

````
python create_indexes.py
````

Output

```
The index idx_sleep created: True
The index idx_sport created: True
The index idx_activity created: True
The index idx_heartrate created: True
```

### Insert data

Data ingestion is done by reading the files with the information captured by the miBand. After recovering your account
files,
insert them into the respective folders in the directory "csv/name_activity".

Run the command below to start the ingest process. A logic of data partitioning and sending via Bulk Operations was
used. Each batch is configured to ingest 30 documents.

````
 python ingestion.py
````

Output

```
Total chunks: 1
Indexing chunk to index idx_sleep...
End indexing chunk.
Total chunks: 1
Indexing chunk to index idx_activity...
End indexing chunk.
Total chunks: 0
End indexing chunk.
Total chunks: 3
Indexing chunk to index idx_heartrate...
Indexing chunk to index idx_heartrate...
Indexing chunk to index idx_heartrate...
End indexing chunk.

```