import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

# Инициализация клиента Elasticsearch
client = Elasticsearch(api_key=os.getenv("API_KEY"), elastic_host=os.getenv("HOST"))

# Имя индекса
index_name = "aboba_index"

# Поиск всех документов в индексе (ограничено по умолчанию 10, можно увеличить "size" при необходимости)
response = client.search(index=index_name, query={"match_all": {}}, size=1000)

# Выводим документы
documents = response['hits']['hits']
for doc in documents:
    print(f"Document ID: {doc['_id']}, Source: {doc['_source']}")
