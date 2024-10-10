import logging
import traceback
from elasticsearch import Elasticsearch

class ElasticsearchHandler(logging.Handler):
    def __init__(self, hosts, api_key, index_name):
        super().__init__()
        self.client = Elasticsearch(hosts=hosts, api_key=api_key)
        self.index_name = index_name

    def emit(self, record):
        # Преобразуем лог-запись в строку
        if self.formatter:
            log_entry = self.format(record)
            timestamp = self.formatter.formatTime(record)
        else:
            log_entry = record.msg
            timestamp = record.created

        # Добавляем traceback, если есть ошибка
        if record.exc_info:
            # Получаем traceback и преобразуем в строку
            exc_info = ''.join(traceback.format_exception(*record.exc_info))
        else:
            exc_info = None

        # Создаем JSON-объект для отправки
        log_document = {
            "message": log_entry,
            "level": record.levelname,
            "timestamp": timestamp,
            "traceback": exc_info  
        }

        # Отправляем данные в Elasticsearch
        self.client.index(index=self.index_name, document=log_document)

class ElasticsearchLogger(object):
    def __init__(self, logger_name='python-logger',
                 elastic_host='https://your-elastic-instance:9200',
                 api_key='your_api_key',
                 index_name='aboba_index'):
        self.logger_name = logger_name
        self.elastic_host = elastic_host
        self.api_key = api_key
        self.index_name = index_name

    def get(self):
        logging.basicConfig(
            format="%(asctime)s %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )

        # Создаем Elasticsearch клиент
        elastic_handler = ElasticsearchHandler(
            hosts=self.elastic_host,
            api_key=self.api_key,
            index_name=self.index_name
        )

        # Устанавливаем форматтер для нашего обработчика
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        elastic_handler.setFormatter(formatter)

        self.stderrLogger = logging.StreamHandler()
        logging.getLogger().addHandler(self.stderrLogger)
        self.logger = logging.getLogger(self.logger_name)

        # Добавляем обработчик для отправки логов в Elasticsearch
        self.logger.addHandler(elastic_handler)
        return self.logger