"""
This file contains the configuration for the project.
"""

import json
from os import getenv

from dotenv import load_dotenv

load_dotenv()

label_map = json.loads(getenv("CONFIG_PARAMS"))
