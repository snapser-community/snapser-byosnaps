# Use an official Python runtime as a parent image
FROM python:3.10-slim

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

# Make port 5003 available to the world outside this container
EXPOSE 5003

# Run Gunicorn to serve the app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5003", "app:app"]
