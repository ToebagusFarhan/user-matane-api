# Use an official lightweight Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Create and set the working directory
WORKDIR /app

# Copy only requirements.txt to leverage Docker caching
COPY app/requirements.txt .

# Install runtime dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the required port
EXPOSE 8080

# Command to run the application
CMD ["python", "app/server.py"]
