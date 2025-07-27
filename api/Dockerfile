# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies early to leverage caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your application code
COPY . .

ARG OPENAI_API_KEY
ARG CATS_API_KEY
ARG STABILITY_API_KEY

ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV CATS_API_KEY=$CATS_API_KEY
ENV STABILITY_API_KEY=$STABILITY_API_KEY

# Expose port and run FastAPI app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]