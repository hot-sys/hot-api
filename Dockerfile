# Utiliser une image légère de Python
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .

# Installer les outils système requis
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    && apt-get clean

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port de l'application
EXPOSE 10000

# Ajouter le script d'entrée (si nécessaire)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Lancer les migrations et le serveur
CMD ["sh", "/app/entrypoint.sh"]
