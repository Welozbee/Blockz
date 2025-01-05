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
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )

        create_tables(conn)

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DATABASE"),
        )
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