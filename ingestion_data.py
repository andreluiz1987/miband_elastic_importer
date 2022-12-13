import json
import os
import pathlib

from elasticsearch import Elasticsearch

from csv import DictReader


def get_client_es():
    return Elasticsearch(
        hosts=[{'host': 'localhost', 'port': 9200}]
    )


def insert_data(datas, idx_name):
    chunks = list(partition(datas, 50))
    print(f'Total chunks: {len(chunks)}')
    for chunk in chunks:
        operations = []
        for data in chunk:
            action = {"index": {"_index": idx_name}}
            doc = json.dumps(data)
            operations.append(action)
            operations.append(doc)
        get_client_es().bulk(index=idx_name, body=operations)
        print(f'Indexing chunk to index {idx_name}...')

    print('End indexing chunk.')


def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_heartrate():
    filename = 'csv/HEARTRATE_AUTO_1670796226726.csv'
    with open(filename, 'r', encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        return list(dict_reader)


if __name__ == '__main__':
    dirs = [item for item in os.listdir("csv") if os.path.isdir(os.path.join("csv", item))]
    data = []
    for name in dirs:
        for files in pathlib.Path(f'csv/{name}').glob('*.csv'):
            with open(files, 'r', encoding='utf-8-sig') as f:
                dict_reader = DictReader(f)
                data = list(dict_reader)
                insert_data(data, f'idx_{name}')

    # heartrate = get_heartrate()
    # insert_data(heartrate)
