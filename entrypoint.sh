#!/bin/sh

# Appliquer les migrations Django
# echo "Applying database migrations..."
# python manage.py migrate

# Démarrer le serveur
echo "Starting server..."
python manage.py runserver 0.0.0.0:${PORT:-10000}
