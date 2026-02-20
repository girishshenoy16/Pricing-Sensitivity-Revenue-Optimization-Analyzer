import pandas as pd
import numpy as np
from src.config import PROCESSED_DATA_PATH

def feature_engineering():
    df = pd.read_csv(PROCESSED_DATA_PATH)

    df["log_quantity"] = np.log(df["quantity"])
    df["log_price"] = np.log(df["price_per_unit"])

    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Feature engineering completed.")