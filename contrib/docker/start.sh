#!/bin/sh
python manage.py migrate --noinput                # Apply database migrations
python manage.py collectstatic --clear --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /app/logs/celery.log
touch /app/logs/gunicorn.log
touch /app/logs/access.log
tail -n 0 -f /app/logs/*.log &

rm -rf celerybeat.pid
celery worker --app=debunkbot.celeryapp:app -l info --hostname=$DOKKU_APP_NAME &> /app/logs/celery.log &
celery beat --app=debunkbot.celeryapp:app -l info &> /app/logs/celery.log &
celery flower --app=debunkbot.celeryapp:app --basic_auth=esirk:Ee199407#@ --broker=$DEBUNKBOT_BROKER_URL -l info &> /app/logs/celery.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers=${DEBUNKBOT_GUNICORN_WORKERS:-3} \
    --worker-class gevent \
    --log-level=info \
    --timeout=${DEBUNKBOT_GUNICORN_TIMEOUT:-60} \
    --log-file=/app/logs/gunicorn.log \
    --access-logfile=/app/logs/access.log \
    --name debunkbot --reload debunkbot.wsgi:application \
    --chdir debunkbot/
