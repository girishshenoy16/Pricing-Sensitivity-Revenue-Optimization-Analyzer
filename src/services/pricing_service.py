import numpy as np
import pandas as pd
from src.model_training.model_registry import load_model
from src.config import DEFAULT_GENDER, DEFAULT_AGE

def predict_quantity(category, price):
    model = load_model(category)

    new_data = pd.DataFrame({
        "log_price": [np.log(price)],
        "gender": [DEFAULT_GENDER],
        "age": [DEFAULT_AGE]
    })

    pred_log_q = model.predict(new_data)[0]
    return np.exp(pred_log_q)

def calculate_revenue(price, quantity):
    return price * quantity

def calculate_profit(price, quantity, cost_ratio):
    cost = price * cost_ratio
    return (price - cost) * quantity