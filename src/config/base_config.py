import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "retail_sales_dataset.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "cleaned_data.csv")

MODEL_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
LOG_DIR = os.path.join(BASE_DIR, "logs")

DEFAULT_GENDER = "Male"
DEFAULT_AGE = 30