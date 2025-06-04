#!/bin/bash
rm -rf staticfiles/*
docker-compose exec web python manage.py collectstatic --noinput --clear