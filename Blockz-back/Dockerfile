# ------ Python ------

# Image de base python
FROM python:3.9 as python
# On utilise le directory /code dans le conteneur pour l'application
WORKDIR /code
# On copie tout le code de l'application dans le dossier /code
COPY . .
# Commande pour installer les dépendances nécessaires pour faire tourner le back
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# On expose le port ou l'api va tourner
EXPOSE 8000
# Commande pour démarrer le container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ------ MySQL ------ 

# Image de base mysql
FROM mysql:8.0 as mysql
# Commande pour set le host et le port correctement
RUN echo "[mysqld]\n\
    bind-address = 0.0.0.0\n\
    port = 3306" > /etc/mysql/conf.d/custom.cnf
# On expose le port ou la bdd va tourner
EXPOSE 3306
# Lancer le serveur MySQL
CMD ["mysqld"]
