# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
