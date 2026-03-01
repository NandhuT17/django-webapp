#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py migrate

python createadmin.py

python manage.py collectstatic --noinput