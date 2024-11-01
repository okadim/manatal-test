# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
