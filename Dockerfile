# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the start script executable
RUN chmod +x start.sh

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV FLASK_APP=app.py

# Run the start script when the container launches
CMD ["/app/start.sh"]