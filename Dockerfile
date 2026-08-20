FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY Advertising.csv .

# Create models directory
RUN mkdir -p models

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_PATH=/app/Advertising.csv
ENV MODEL_PATH=/app/models/model.pkl
ENV METRICS_PATH=/app/models/metrics.json

# Default command runs training
CMD ["python", "src/train.py"]
