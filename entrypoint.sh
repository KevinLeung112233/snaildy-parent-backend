#!/bin/sh

# Wait for database to be ready
echo "Waiting for database..."
python /app/db_checker.py

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Start Gunicorn
exec gunicorn snaildy_parent_backend.wsgi:application --bind 0.0.0.0:8000