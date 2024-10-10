from opensearch_logger import Log, OpenSearchClient
from opensearch_dsl import Search


def main():
    index_name = 'logs-index'
    index_body = {
        'settings': {
            'index': {
                'number_of_shards': 1  # количество шардов
            }
        }
    }

    # Создаем клиент OpenSearch
    os_client = OpenSearchClient()
    # os_client.create_index(index_name, index_body)

    # Инициализация структуры документа
    Log.init(using=os_client.client)

    # Запись логов в индекс
    log_entries = [
        Log(meta={'id': 1}, message='Первый лог', timestamp='2024-10-10T10:00:00'),
        Log(meta={'id': 2}, message='Второй лог', timestamp='2024-10-10T10:05:00'),
        Log(meta={'id': 3}, message='Третий лог', timestamp='2024-10-10T10:10:00')
    ]

    for log_entry in log_entries:
        response = log_entry.save(using=os_client.client)
        print('Лог добавлен:', response)

    # Поиск логов
    s = Search(using=os_client.client, index=index_name).query('match', message='Первый лог')
    # s = Log.search().filter('term', timestamp='2024-10-10T10:00:00').query()
    response = s.execute()

    # Вывод результатов поиска
    print('Результаты поиска:')
    for hit in response:
        print(hit.meta.score, hit.message)

    # # Удаление документа
    # Log.init(using=os_client.client)
    # delete_response = Log.get(id=1, using=os_client.client).delete()
    # print('Документ удален:', delete_response)

    # # Удаление индекса
    # os_client.delete_index(index_name)

if __name__ == '__main__':
    main()
