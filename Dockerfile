FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier tout le contenu du projet
COPY . .

# Exposer le port
EXPOSE 10000

# Ajouter le script d'entrée
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Commande par défaut pour lancer l'application
CMD ["sh", "/app/entrypoint.sh"]
