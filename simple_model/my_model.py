from typing import List

import joblib
import pandas as pd

import mlserver
import numpy as np
from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse

class SimpleModel(MLModel):

    async def load(self):
        self.model = joblib.load("model.pkl")
        mlserver.register("requests_with_nan_features", "Количество запросов с недостатком фичей")
        mlserver.register("test_metric", "Тестовая метрика")

    
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        
        payload = self._check_request(payload)
        data = self.get_data_vector(payload)
        self.log_nan_values(data)
        
        mlserver.log(test_metric=1)

        prediction = self.model.predict(data)
        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[NumpyCodec.encode_output(name="predict", payload=prediction)],
        )
    
    def get_data_vector(self, inf_request: InferenceRequest) -> np.array:
        """Функция для обработки и преобразования запроса к pandas.DataFrame"""

        data_vector_list = []
        for item in inf_request.inputs:
            data_vector_list.append(item.data)
        data_vector = np.array(data_vector_list)

        return data_vector
    
    @staticmethod
    def log_nan_values(values: np.array) -> None:
        print(values)
        has_nan = np.isnan(values).any()
        
        if has_nan:
            mlserver.log(requests_with_nan_features=1)

    def _check_request(self, payload: InferenceRequest) -> InferenceRequest:
        """Функция валидации запроса (замена всех None на np.nan)"""

        for item in payload.inputs:
            item.data.root = [
                np.nan if data is None else data for data in item.data.root
            ]
        return payload