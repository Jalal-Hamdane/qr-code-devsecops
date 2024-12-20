# Utilisation d'une image légère de Node.js
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY package.json package-lock.json ./

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers
COPY . .

# Construire l'application pour la production
RUN npm run build

# Exposer le port pour l'application
EXPOSE 3000

# Commande pour démarrer le serveur Next.js
CMD ["npm", "start"]
