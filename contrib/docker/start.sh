#!/bin/sh
python manage.py migrate --noinput                # Apply database migrations
python manage.py collectstatic --clear --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /src/logs/celery.log
touch /app/logs/gunicorn.log
touch /app/logs/access.log
tail -n 0 -f /app/logs/*.log &

celery -A debunkbot worker --app=debunkbot.celeryapp:app -l info &> /src/logs/celery.log  
celery -A debunkbot beat --app=debunkbot.celeryapp:app -l info &> /src/logs/celery.log  &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gevent \
    --log-level=info \
    --log-file=/app/logs/gunicorn.log \
    --access-logfile=/app/logs/access.log \
    --name debunkbot --reload debunkbot.wsgi:application \
    --chdir debunkbot/
