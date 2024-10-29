# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables:
# this one is old because i was using pinecone before faiss, kept it in case i want to use it again
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
