import os

env = os.getenv("PRICINGAI_ENV", "development")

if env == "production":
    from .prod_config import *
else:
    from .dev_config import *