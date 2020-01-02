#!/bin/sh
nginx
source venv/bin/activate
exec gunicorn -b  :2000 --workers 1 --access-logfile - --error-logfile - wsgi:app
