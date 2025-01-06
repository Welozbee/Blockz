# ------- Base -------

# Utiliser l'image officielle de Node.js comme image parente
FROM node:22 AS base
# Définir le répertoire de travail
WORKDIR /app
# Copier package.json
COPY . .
# Installer les dépendances de l'application
RUN npm install -g @angular/cli
RUN npm install --include=dev

# ------- Dev -------

# Utiliser la base pour le stage dev
FROM base AS dev
# Exposer le port sur lequel l'application va s'éxecuter
EXPOSE 4200
# Exécuter l'application
CMD ["ng", "serve","--poll", "2000", "--host", "0.0.0.0"]

# ------- Build -------

# Utiliser la base pour le stage build
FROM base AS build
# Build l'application
RUN ng build

# ------- Prod -------

# Utiliser l'image nginx pour le stage prod
FROM nginx:alpine AS prod
# Supprimer les fichier inutiles
RUN rm /usr/share/nginx/html/*
# Depuis le stage build copier la sortie du build et l'utiliser
COPY --from=build /app/dist/browser /usr/share/nginx/html
# Exposer le port sur lequel l'application va s'éxecuter
EXPOSE 80
# Exécuter l'application
CMD ["nginx", "-g", "daemon off;"]