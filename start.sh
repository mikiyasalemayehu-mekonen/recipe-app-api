#!/bin/sh

set -e

cd /app

/py/bin/python manage.py wait_for_db
/py/bin/python manage.py migrate
/py/bin/python manage.py collectstatic --no-input
# Use Render's PORT or fallback to 8000
/py/bin/uwsgi --http :${PORT:-8000} --workers 2 --master --enable-threads --module app.wsgi
