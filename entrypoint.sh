#!/bin/bash

# Move to project directory
# shellcheck disable=SC2164
cd /my_spending_admin

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser for Django
echo "Create superuser for Django"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists() or User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python manage.py shell

# Set keys in Django project
echo "Set keys in Django project"
python manage.py filldb

# Load DB data from fixture
echo "Load DB data from fixture"
python manage.py loaddata spending_fixture.json

# Start celery
echo "Starting celery"
celery -A myspending worker -l INFO -B &

# Start server through gunicorn
echo "Starting server through gunicorn"
gunicorn --bind 0.0.0.0:8000 myspending.wsgi:application