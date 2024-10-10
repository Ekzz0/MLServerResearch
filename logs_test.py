import os
from elasticsearch_logger import ElasticsearchLogger
from dotenv import load_dotenv

load_dotenv()

# Пример использования
logger = ElasticsearchLogger(api_key=os.getenv("API_KEY"), elastic_host=os.getenv("HOST")).get()
logger.info("This is a test log message sent to Elasticsearch.")


count = 0
from time import sleep
while True:

    count = count + 1

    if count % 2 == 0:
        logger.error('Error Message Code Faield :{} '.format(count))
    else:
        logger.info('python-logstash: test logstash info message:{} '.format(count))
    sleep(2)
