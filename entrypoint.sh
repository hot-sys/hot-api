#!/bin/bash

# Démarrer Redis en arrière-plan
redis-server /etc/redis/redis.conf &

# Attendre que Redis soit prêt
until redis-cli -h 127.0.0.1 -p 6379 ping > /dev/null 2>&1; do
    echo "Waiting for Redis to start..."
    sleep 1
done

# Appliquer les migrations Django
python manage.py migrate

# Démarrer le serveur Django
exec python manage.py runserver 0.0.0.0:${PORT:-8000}