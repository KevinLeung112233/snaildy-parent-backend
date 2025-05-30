FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (netcat for database check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . /app/

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

RUN python manage.py collectstatic --noinput -v 3

# Collect static files
RUN python manage.py collectstatic --noinput -v 3


RUN chown -R 1000:1000 /app/staticfiles

# RUN python manage.py makemigrations
# RUN python manage.py migrate



# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]