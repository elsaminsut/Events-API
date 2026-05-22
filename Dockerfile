# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in Docker container
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Export port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]