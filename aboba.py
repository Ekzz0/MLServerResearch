


import requests
import numpy as np
from mlserver.codecs import NumpyRequestCodec

# Корректный формат для отправки запроса
array = np.array([[1, 1, np.nan]])
inference_request = NumpyRequestCodec.encode_request(array)
raw_request = inference_request.dict()

# Отправляем запрос на сервер
r = requests.post('http://0.0.0.0:8080/v2/models/simple-model/infer', json=raw_request)

# Выводим ответ
print(r.json())
