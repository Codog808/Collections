# Use slim Python image as the base
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first for caching dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . /app

# Set working directory to server for FastAPI
WORKDIR /app/server

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run FastAPI server
CMD ["python", "main.py"]
