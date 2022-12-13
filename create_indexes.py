import json
import pathlib

from elasticsearch import Elasticsearch


def get_client_es():
    return Elasticsearch(
        hosts=[{'host': 'localhost', 'port': 9200}]
    )


def get_mappings():
    dict = {}
    for filename in pathlib.Path('mappings').glob('*.json'):
        f = open(filename, "r")
        dict[filename.stem] = json.loads(f.read())
    return dict


if __name__ == '__main__':
    mappings = get_mappings()
    for index_name, mapping in mappings.items():
        response = get_client_es().indices.create(index=index_name, body=mapping, ignore=400)
        if "acknowledged" in response and response["acknowledged"]:
            print(f'The index {index_name} created: {response["acknowledged"]}')
        else:
            print(f'Failed create index {index_name} reason: {response["error"]["reason"]}')
