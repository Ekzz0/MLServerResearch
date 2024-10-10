from opensearchpy import OpenSearch
from opensearch_dsl import Document, Text, connections, Search
from datetime import datetime

# Настройки подключения
class OpenSearchClient:
    def __init__(self, host='83.166.232.242', port=9200, auth=('admin', 'lafogu26Q!')):
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )
        connections.add_connection('default', self.client)

    def create_index(self, index_name, index_body):
        try:
            response = self.client.indices.create(index_name, body=index_body)
            print('Индекс создан:', response)
        except Exception as e:
            print('Ошибка при создании индекса:', e)

    def delete_index(self, index_name):
        response = self.client.indices.delete(index=index_name)
        print('Индекс удален:', response)

    def log(self, message: str, level: str = "INFO", traceback: str = None, index='logs-index'):
        """Метод для логирования сообщений в OpenSearch"""
        current_timestamp = datetime.now().isoformat()  # Получаем текущее время
        log_body = {
            'message': message,
            'level': level,  # Уровень логирования
            'timestamp': current_timestamp  # Используем текущее время
        }

        if traceback:  # Добавляем traceback, если он есть
            log_body['traceback'] = traceback

        self.client.index(
            index=index,
            body=log_body
        )

# Определение структуры документа
class Log(Document):
    message = Text()
    timestamp = Text()
    level = Text()
    traceback = Text()

    class Index:
        name = 'logs-index'