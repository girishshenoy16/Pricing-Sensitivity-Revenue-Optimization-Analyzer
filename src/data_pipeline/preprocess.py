import pandas as pd
import os
from src.utils.logger import get_logger
from src.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

def preprocess():
    df = pd.read_csv(RAW_DATA_PATH)

    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.dropna()

    df = df[(df["price_per_unit"] > 0) & (df["quantity"] > 0)]

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)


    logger = get_logger("Preprocess")

    logger.info("Data preprocessing completed.")
