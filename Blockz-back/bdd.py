import os
import mysql.connector
from dotenv import load_dotenv
import sqlite3
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
ENV = os.getenv("ENV", "DEV").upper()

def get_connection(seed: bool = False):
    if ENV == "DEV":
        conn = sqlite3.connect(os.path.join(BASE_DIR, "Blockz.db"))
        conn.execute("PRAGMA foreign_keys = ON;") # TODO: Que fait cette ligne?
        print("Dev environment detected, Sqlite3 launched")
        create_tables(conn)
        if seed or _should_seed_dev(conn):
            insert_data(conn)
        return conn


    # Connexion à MySQL
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        passwd=os.getenv("MYSQL_ROOT_PASSWORD"),
        port="3306",
    )
    
    # Créer la DB si elle existe pas et la selectionne
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
    cur.execute(f"USE {MYSQL_DB}")
    cur.close()

    create_tables(conn)  # Crée les tables au besoin

    # Connexion avec la base de données
    conn.database = "blockz"

    if seed:
        insert_data(conn)
    return conn

# Ouvre le fichier create_bdd_prod.sql et execute le fichier pour créer les tables
def create_tables(conn):
    sql_file = "Blockz-bdd/create_bdd_dev.sql" if ENV == "DEV" else "Blockz-bdd/create_bdd_prod.sql"
    run_sql_file(conn, sql_file)

def insert_data(conn):
     run_sql_file(conn, "Blockz-bdd/fill_blocks.sql")

def _should_seed_dev(conn) -> bool:
    if not isinstance(conn, sqlite3.Connection):
        return False
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM blocks")
        count = cur.fetchone()[0]
        return count == 0
    except Exception:
        return False
    finally:
        cur.close()


def run_sql_file(conn, path: str):
    abs_path = os.path.join(BASE_DIR, path)
    with open(abs_path, "r", encoding="utf-8") as f:
        sql = f.read().strip()
        if not sql:
            return

    if isinstance(conn, sqlite3.Connection):
        conn.executescript(sql)
        conn.commit()
        return

    cur = conn.cursor()
    try:
        for _ in cur.execute(sql, multi=True):
            pass
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
