import joblib
import traceback as tb
import mlserver
import numpy as np
from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse
from opensearch_logger import Log, OpenSearchClient


class SimpleModel(MLModel):

    async def load(self):
        self.model = joblib.load("model.pkl")

        # Инициализация клиента OpenSearch
        self.logger_client = OpenSearchClient()  # Создайте экземпляр вашего клиента
        Log.init(using=self.logger_client.client)  # Инициализация структуры документа для логов

        mlserver.register("requests_with_nan_features", "Количество запросов с недостатком фичей")
        mlserver.register("test_metric", "Тестовая метрика")

    
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:    
        try:
            # Логирование входного запроса
            self.logger_client.log(f"Received request with payload: {payload}", level="INFO")
            
            payload = self._check_request(payload)
            data = self.get_data_vector(payload)

            # Логирование метрики NaN значений в фичах
            has_nan = np.isnan(data).any()
            if has_nan:
                mlserver.log(requests_with_nan_features=1)

                # Логируем в OpenSearch
                self.logger_client.log(f"Request contains NaN values in features. Model: {self.name}, Payload: {payload}", level="WARNING")

            # Получение предсказания от модели
            prediction = self.model.predict(data)
            self.logger_client.log(f"Prediction: {prediction}", level="INFO")

            # Формирование ответа
            response = InferenceResponse(
                model_name=self.name,
                model_version=self.version,
                outputs=[NumpyCodec.encode_output(name="predict", payload=prediction)],
            )

            # Логирование успешного завершения
            self.logger_client.log(f"Inference successful for model {self.name} v{self.version}", level="INFO")
            return response
        except Exception as e:
            # Логирование исключений с деталями
            tb_str = tb.format_exc()  # Получаем traceback
            self.logger_client.log(f"Error during inference: {str(e)}", level="ERROR", traceback=tb_str)
            # raise e
    
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