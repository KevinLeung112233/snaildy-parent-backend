#!/bin/sh

# Wait for database to be ready
echo "Waiting for database..."
python /app/db_checker.py

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput


# Create cache table if using database cache
# python manage.py createcachetable

# Collect static files on every startup (development only)
if [ "$DJANGO_DEBUG" = "True" ]; then
    python manage.py collectstatic --noinput
fi

# Start Gunicorn
exec gunicorn snaildy_parent_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug