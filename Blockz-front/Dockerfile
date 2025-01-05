# Utiliser l'image officielle de Node.js comme image parente
FROM node:22 AS base
# Définir le répertoire de travail
WORKDIR /usr/src
# Copier package.json
COPY . .
# Installer les dépendances de l'application
RUN npm install -g @angular/cli
RUN npm install --include=dev

FROM base AS dev
# Exposer le port sur lequel l'application s'exécute
EXPOSE 4200
# Exécuter l'application
CMD ["ng", "serve", "--host", "0.0.0.0"]

FROM base AS build
RUN ng build

FROM nginx:alpine AS prod
RUN rm /usr/share/nginx/html/*
COPY --from=build /usr/src/dist/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]