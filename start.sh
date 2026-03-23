#!/bin/sh

set -e

/py/bin/python manage.py wait_for_db
/py/bin/python manage.py migrate
/py/bin/python manage.py collectstatic --no-input
/py/bin/uwsgi --http :8000 --workers 2 --master --enable-threads --module app.wsgi
