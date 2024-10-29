# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install build-essential and gcc
RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    apt-get clean

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install uvicorn and streamlit if they are not in the requirements.txt
RUN pip install uvicorn streamlit

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the entire application into the container
COPY . ./

# Expose the ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Set environment variables to prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run both FastAPI (with Uvicorn) and Streamlit with a delay to ensure Uvicorn starts first
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & sleep 30 && streamlit run app_interface.py --server.port 8501 --server.address 0.0.0.0"]
