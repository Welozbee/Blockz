import bdd

# Connexion à la base de données + Tout préparer
conn = bdd.get_connection()

# Test pour tout recevoir
cursor = conn.cursor()
cursor.execute("SELECT * FROM blocks")
result = cursor.fetchall()
print(result)


# TODO: Faire l'api rest