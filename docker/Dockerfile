# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ../requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of the code
COPY .. .
ENV PYTHONPATH=/app

# Run Alembic migrations and launch app
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
