![Logo du projet](Blockz-front\src\assets\Blockz.png)


## Table des Matières

- [Nom du Projet](#nom-du-projet)
  - [Table des Matières](#table-des-matières)
  - [Description](#description)
  - [Architecture du projet](#architecture-du-projet)
  - [Utilisation](#utilisation)
    - [Prérequis](#prérequis)
    - [Lancement de l'environement DEV](#lancement-de-lenvironement-dev)
    - [Lancement de l'environement PROD](#lancement-de-lenvironement-prod)
  - [Differences entre les environements](#differences-entre-les-environements)
    - [Dev](#dev)
    - [Prod](#prod)

## Description

Ce projet a été développé dans le cadre du module 347 de l'EPSIC. L'objectif est une application répertoriant les blocs de Minecraft ainsi que leurs propriétés (images non incluses)

## Architecture du Projet

Le projet utilise une architecture multiconteneur pour isoler les différents composants de l'application. Voici une vue d'ensemble de l'architecture :

- **Frontend (Angular) :** L'interface utilisateur de l'application web.
- **Backend (FastAPI - Python) :** La logique métier et les API pour interagir avec la base de données.
- **Base de Données (MySQL - Production, SQLite - Développement) :** Stockage des données de l'application.

## Utilisation
### Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

1. [Docker](https://docs.docker.com/desktop/?_gl=1*tqgetu*_ga*MTQ0NzcyMzE2MC4xNjk0MDc0NDc0*_ga_XJWPQMJYHQ*MTcwMzU3ODE1My4xNC4xLjE3MDM1NzgxNTMuNjAuMC4w)

2. [Docker Compose](https://docs.docker.com/compose/)

Assurez-vous que ces prérequis sont correctement installés avant de poursuivre avec les étapes suivantes.

### Lancement de l'environement DEV
```bash
docker compose  -f "docker-compose.dev.yml" up -d --build
```

### Lancement de l'environement PROD
```bash
docker compose -f "docker-compose.prod.yml" up -d --build 
```

## Différences entre les environements

### Dev
- Le code du frontend est modifiable en temps réel.
- On utilise le moteur de base de donnés SQLlite.

### Prod
- Le code du frontend n'est pas modifiable sans devoir rebuild.
- On utilise le moteur de base de données MySQL.

## Tester les Différences
On peut voir en faisant Docker ps, on peut voir que, dans un environnement de développement, nous n'avons que 2 conteneurs, alors que si on le lance en production, on aura le conteneur du serveur MySQL qui se rajoute au lot.

On peut voir que si nous modifions le code source du front-end en mode développement, l'application se mettra automatiquement à jour. À l'inverse, en production, le code est compilé et donc non modifiable sans devoir refaire le build.

## Réalisation

- Mathieu Rais
- Daniel Baiao

DEVA2A