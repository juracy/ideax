#!/bin/bash

LOG_LEVEL=${LOG_LEVEL:-"info"}

cd /app

export DJANGO_SETTINGS_MODULE=ideax.settings
pip install -r /app/requirements.txt

python manage.py collectstatic --no-input

# TODO: Encontrar método melhor de aguardar o banco de dados
sleep 5

python manage.py migrate
python manage.py compilemessages

if [ ! -f /provisioned ]; then
  echo "First time setup"
  python manage.py loaddata initialdata.json
  touch /provisioned
fi

exec gunicorn ideax.wsgi:application \
    --name ideax_django \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=${LOG_LEVEL} \
"$@"
