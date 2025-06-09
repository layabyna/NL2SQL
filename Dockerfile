# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask default port
EXPOSE 5000

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Set Flask environment variables (optional but useful)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["python", "app.py"]
