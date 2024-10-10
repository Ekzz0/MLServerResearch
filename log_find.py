from elasticsearch import Elasticsearch
from config import HOST, API_KEY


# Инициализация клиента Elasticsearch
client = Elasticsearch(api_key=API_KEY, elastic_host=HOST)

# Имя индекса
index_name = "aboba_index"

# Поиск всех документов в индексе (ограничено по умолчанию 10, можно увеличить "size" при необходимости)
response = client.search(index=index_name, query={"match_all": {}}, size=1000)

# Выводим документы
documents = response['hits']['hits']
for doc in documents:
    print(f"Document ID: {doc['_id']}, Source: {doc['_source']}")
