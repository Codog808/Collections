# Base Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# First, copy only requirements.txt for dependency installation
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app after dependencies are installed
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the app
CMD ["python", "display_app.py"]

