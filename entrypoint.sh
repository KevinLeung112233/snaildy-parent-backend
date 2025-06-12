#!/bin/sh

# Exit immediately on error
set -e

# Wait for database
echo "Waiting for database..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done
echo "Database ready!"

#load default fixed data
find . -name "*.json" -path "*/fixtures/*" -exec python manage.py loaddata {} \;

# Apply migrations
# python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL || true
# Collect static files
python manage.py collectstatic --noinput

# Calculate workers based on available CPUs
workers=$(( $(nproc) * 2 + 1 ))
# Cap at 4 workers for memory efficiency
if [ $workers -gt 4 ]; then
    workers=4
fi


# Choose server based on environment
# if [ "$DJANGO_ENV" = "development" ]; then
#   # Development: Django runserver with auto-reload
#   exec python manage.py runserver 0.0.0.0:8000
# else
  # Production: Gunicorn
exec gunicorn snaildy_parent_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers $(( $(nproc) * 2 + 1 )) \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --timeout 120
# fi