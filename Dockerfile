# Use an official lightweight Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app /app

# Expose the required port
EXPOSE 8080

# Command to run the application
CMD ["python", "server.py"]
