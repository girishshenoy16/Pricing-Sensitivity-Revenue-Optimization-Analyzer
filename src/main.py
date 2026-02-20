import time
import sys

from src.data_pipeline.preprocess import preprocess
from src.data_pipeline.feature_engineering import feature_engineering
from src.model_training.train_elasticity import train_models
from src.utils.logger import get_logger
from src.config import ENVIRONMENT

logger = get_logger("Pipeline")


def run_stage(stage_name, stage_function):
    """
    Runs an individual pipeline stage with timing and error handling.
    """
    logger.info(f"Starting stage: {stage_name}")
    start_time = time.time()

    try:
        stage_function()
        duration = time.time() - start_time
        logger.info(f"Completed stage: {stage_name} in {duration:.2f} seconds")
    except Exception as e:
        logger.exception(f"Stage failed: {stage_name}")
        raise e


def run_pipeline():
    """
    Main pipeline orchestrator.
    """
    logger.info("=" * 60)
    logger.info(f"PricingAI Pipeline Started | Environment: {ENVIRONMENT}")
    logger.info("=" * 60)

    pipeline_start = time.time()

    try:
        # Stage 1: Data Preprocessing
        run_stage("Data Preprocessing", preprocess)

        # Stage 2: Feature Engineering
        run_stage("Feature Engineering", feature_engineering)

        # Stage 3: Model Training
        run_stage("Model Training", train_models)

        total_duration = time.time() - pipeline_start

        logger.info("=" * 60)
        logger.info(f"Pipeline completed successfully in {total_duration:.2f} seconds")
        logger.info("=" * 60)

    except Exception:
        logger.error("Pipeline terminated due to failure.")
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()