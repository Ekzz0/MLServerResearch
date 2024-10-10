import joblib
from elasticsearch_logger import ElasticsearchLogger
import mlserver
import numpy as np
from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse
from config import HOST, API_KEY


class SimpleModel(MLModel):

    async def load(self):
        self.model = joblib.load("model.pkl")
        self.logger = ElasticsearchLogger(api_key=API_KEY, elastic_host=HOST).get()

        mlserver.register("requests_with_nan_features", "Количество запросов с недостатком фичей")
        mlserver.register("test_metric", "Тестовая метрика")

    
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:    
        try:
            # Логирование входного запроса. Но тут может быть персоналка
            self.logger.info(f"Received request with payload: {payload}")
            
            payload = self._check_request(payload)
            data = self.get_data_vector(payload)

            # Логирование метрики NaN значений в фичах
            has_nan = np.isnan(data).any()
            if has_nan:
                mlserver.log(requests_with_nan_features=1)

                 # Логируем в Elasticsearch. Но тут может быть персоналка
                self.logger.warning(f"Request contains NaN values in features. Model: {self.name}, Payload: {payload}")

            # Получение предсказания от модели
            prediction = self.model.predict(data)
            self.logger.info(f"Prediction: {prediction}")

            # Формирование ответа
            response = InferenceResponse(
                model_name=self.name,
                model_version=self.version,
                outputs=[NumpyCodec.encode_output(name="predict", payload=prediction)],
            )

            # Логирование успешного завершения
            self.logger.info(f"Inference successful for model {self.name} v{self.version}")
            return response
        except Exception as e:
            # Логирование исключений с деталями
            self.logger.error(f"Error during inference: {str(e)}", exc_info=True)
            raise e
    
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