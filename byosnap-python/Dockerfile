# syntax=docker/dockerfile:1

#FROM python:3.8-slim-buster
FROM python:3.9

# Create a working directory
WORKDIR /app

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the local code
COPY . .

# Run Server
CMD [ "sh", "run_dev_server.sh"]
