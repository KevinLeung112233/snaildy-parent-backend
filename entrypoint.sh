#!/bin/sh

# Exit immediately on error
set -e

# Wait for database
echo "Waiting for database..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done
echo "Database ready!"

# Apply migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Calculate workers based on available CPUs
workers=$(( $(nproc) * 2 + 1 ))
# Cap at 4 workers for memory efficiency
if [ $workers -gt 4 ]; then
    workers=4
fi


# Start Gunicorn
exec gunicorn snaildy_parent_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers $(( $(nproc) * 2 + 1 )) \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 120