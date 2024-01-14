import logging
import os
from enum import Enum


class Tags(str, Enum):
    # https://fastapi.tiangolo.com/tutorial/metadata/#use-your-tags
    user = "user"


DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

logging.basicConfig(level=logging.INFO if DEBUG else logging.DEBUG)
