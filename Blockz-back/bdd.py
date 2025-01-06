import os
import mysql.connector
from dotenv import load_dotenv
import sqlite3
load_dotenv()

def get_connection():
    if os.getenv("ENV") == "DEV":
        conn = sqlite3.connect("Blockz.db")
        print("Dev environment detected, Sqlite3 launched")
        create_tables(conn)
        insert_data(conn)
    else:
            # Connexion à MySQL
            conn = mysql.connector.connect(
                host="mysql",
                user="root",
                passwd=os.getenv("MYSQL_ROOT_PASSWORD"),
                port="3306",
            )
            create_tables(conn)  # Crée les tables au besoin

            # Connexion avec la base de données
            conn.database = "blockz"
            insert_data(conn)
    return conn

# Ouvre le fichier create_bdd_prod.sql et execute le fichier pour créer les tables
def create_tables(conn):
    if os.getenv("ENV") == "DEV":
        with open('Blockz-bdd/create_bdd_dev.sql', 'r') as file:
            sql_script = file.read()
    else:
        with open('Blockz-bdd/create_bdd_prod.sql', 'r') as file:
            sql_script = file.read()
    cursor = conn.cursor()
    for statement in sql_script.split(";"):
        cursor.execute(statement)
    conn.commit()

def insert_data(conn):
    with open('Blockz-bdd/fill_blocks.sql', 'r') as file:
        sql_script = file.read()
    cursor = conn.cursor()
    for statement in sql_script.split(";"):
        cursor.execute(statement)
    conn.commit()