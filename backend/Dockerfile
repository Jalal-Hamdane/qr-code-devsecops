# Backend Dockerfile
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier le fichier .env dans le conteneur
COPY .env /app/.env


# Copier le code
COPY . .

# Exposer le port de l'API
EXPOSE 8000

# Commande pour démarrer le serveur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
