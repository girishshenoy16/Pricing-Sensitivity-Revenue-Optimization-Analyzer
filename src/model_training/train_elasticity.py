import pandas as pd
import numpy as np
import statsmodels.api as sm
import os
from src.config import PROCESSED_DATA_PATH, OUTPUT_DIR
from src.model_training.model_registry import save_model
from src.utils.logger import get_logger

logger = get_logger("ModelTraining")


def train_models():
    df = pd.read_csv(PROCESSED_DATA_PATH)

    df["log_quantity"] = np.log(df["quantity"])
    df["log_price"] = np.log(df["price_per_unit"])

    results = []

    for category in df["product_category"].unique():
        cat_df = df[df["product_category"] == category]

        if len(cat_df) < 30:
            continue

        X = sm.add_constant(cat_df["log_price"])
        y = cat_df["log_quantity"]

        model = sm.OLS(y, X).fit()

        alpha = model.params["const"]
        beta = model.params["log_price"]

        # 🚨 Economic constraint
        if beta >= 0:
            logger.warning(
                f"{category}: Positive elasticity detected ({beta:.3f}). Applying constraint."
            )
            beta = -0.5  # Force mild inelastic behavior

        save_model(model, category)

        results.append({
            "product_category": category,
            "alpha": alpha,
            "beta": beta,
            "r_squared": model.rsquared
        })

        logger.info(f"{category} | Final Elasticity (beta): {beta:.3f}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pd.DataFrame(results).to_csv(
        os.path.join(OUTPUT_DIR, "elasticity_summary.csv"),
        index=False
    )

    logger.info("Elasticity training completed successfully.")