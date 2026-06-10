#!/bin/bash
# Collect static files
cd elif_universe
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput
