# Use a slim base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir flask requests python-dotenv pymongo torch transformers flask-cors

# Make port 9050 available to the world outside this container
EXPOSE 9050

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=9050"]
