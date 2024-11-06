## How to Run the Project

This project consists of a FastAPI backend and a Streamlit user interface. You can run both using Docker. Follow these steps to get started:

### Prerequisites

- Install [Docker](https://docs.docker.com/get-docker/).

### Steps to Run the Project

1. **Build the Docker Image**

   Make sure you are in the root directory of the project (where the Dockerfile is located). Then, build the Docker image by running:
```
   docker build -t job-matching-app .
```


2. **Run the Docker Container**

After successfully building the image, run a container from it:
```
docker run -p 8000:8000 -p 8501:8501 job-matching-app
```

This will:

Expose the FastAPI application on port 8000.
Expose the Streamlit user interface on port 8501.
3. **Access the Application**

FastAPI Documentation: You can access the FastAPI Swagger UI for API documentation at http://localhost:8000/docs.
Streamlit Interface: You can access the Streamlit UI at http://localhost:8501.
### Additional Information
To edit the data (e.g., job postings or candidates), modify the JSON files under the /data directory.
The generate_100k_mock.py script can be used to generate mock candidate data for testing purposes.
