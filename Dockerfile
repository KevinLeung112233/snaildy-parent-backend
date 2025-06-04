FROM python:3.12-slim-bullseye  

# Security optimizations
RUN adduser --system --group --no-create-home django
RUN mkdir /app && chown django:django /app

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=django:django . .

RUN mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Switch to non-root user
USER django

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]