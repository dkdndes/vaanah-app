#!/bin/sh
​
set -e
​
python manage.py collectstatic --noinput
​
uwsgi --socket :4300 --master --enable-threads --module app.wsgi