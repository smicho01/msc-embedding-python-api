# Use a smaller base image
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN apk add --no-cache build-base

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir flask requests python-dotenv pymongo torch-cpu transformers flask-cors \
    && apk del build-base

# Make port 9050 available to the world outside this container
EXPOSE 9050

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=9050"]
