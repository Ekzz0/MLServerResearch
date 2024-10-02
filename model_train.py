# import numpy as np
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# import joblib
# # Генерация данных
# # Пусть y = X1 + X2 + X3 + шум
# np.random.seed(42)  # для воспроизводимости
# X = np.random.rand(10000, 3)  # 1000 строк и 3 фичи
# noise = np.random.normal(0, 0.1, size=(10000,))
# y = X[:, 0] + X[:, 1] + X[:, 2] + noise  # y = X1 + X2 + X3 + шум

# # Разделение на тренировочный и тестовый наборы данных
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Создание и обучение модели линейной регрессии
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Предсказание на тестовом наборе
# y_pred = model.predict(X_test)

# # Оценка модели
# mse = mean_squared_error(y_test, y_pred)
# print(f"Mean Squared Error: {mse}")
# print("Коэффициенты модели (должны быть близки к 1):", model.coef_)
# print("Свободный член (должен быть близок к 0):", model.intercept_)

# joblib.dump(model, "model.pkl")