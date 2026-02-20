import numpy as np
import joblib
import os
from src.config import MODEL_DIR

def simulate_curve(category, avg_price, cost_ratio):
    model_path = os.path.join(MODEL_DIR, f"{category}_model.pkl")
    model = joblib.load(model_path)

    alpha = model.params["const"]
    beta = model.params["log_price"]

    price_range = np.linspace(avg_price * 0.5, avg_price * 1.5, 120)

    revenues = []
    profits = []

    for P in price_range:
        Q = np.exp(alpha) * (P ** beta)
        R = P * Q
        Profit = (P - P * cost_ratio) * Q

        revenues.append(R)
        profits.append(Profit)

    optimal_index = profits.index(max(profits))
    optimal_price = price_range[optimal_index]
    optimal_profit = profits[optimal_index]

    return price_range, revenues, profits, optimal_price, optimal_profit