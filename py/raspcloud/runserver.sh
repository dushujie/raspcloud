#! /bin/sh

python manage.py runserver 0.0.0.0:8000 &
python -m SimpleHTTPServer 8001 &
