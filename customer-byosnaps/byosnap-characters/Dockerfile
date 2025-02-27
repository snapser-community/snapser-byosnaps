# # syntax=docker/dockerfile:1

# #FROM python:3.8-slim-buster
# FROM python:3.9

# # Create a working directory
# WORKDIR /app

# # Install requirements
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

# # Copy the local code
# COPY . .

# # Run Server
# CMD [ "sh", "run_dev_server.sh"]

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  g++ \
  build-essential \
  libffi-dev

# Clean up the apt cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Gunicorn
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY . /app

WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Install TextBlob and download necessary NLTK corpora
# RUN pip install textblob
# RUN python -m textblob.download_corpora
# # Download necessary NLTK corpora used by TextBlob
# RUN python -m nltk.downloader punkt
# RUN python -m nltk.downloader punkt_tab
# RUN python -m nltk.downloader averaged_perceptron_tagger
# RUN python -m nltk.downloader brown

# Make port 5003 available to the world outside this container
EXPOSE 5003

# Run Gunicorn to serve the app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5003", "app:app"]
