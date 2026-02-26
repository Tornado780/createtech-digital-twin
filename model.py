import numpy as np
from sklearn.linear_model import LinearRegression

def train_model():
    np.random.seed(42)
    data_size = 200

    rain = np.random.uniform(0, 10, data_size)
    labor = np.random.uniform(50, 120, data_size)
    material_delay = np.random.uniform(0, 5, data_size)
    productivity = np.random.uniform(0.7, 1.2, data_size)

    delay = (
        0.7 * rain
        - 0.04 * labor
        + 1.5 * material_delay
        - 5 * productivity
        + np.random.normal(0, 1, data_size)
    )

    X = np.column_stack((rain, labor, material_delay, productivity))
    y = delay

    model = LinearRegression()
    model.fit(X, y)

    return model

def predict_delay(model, rain, labor, material_delay, productivity):
    prediction = model.predict([[rain, labor, material_delay, productivity]])
    return max(prediction[0], 0)