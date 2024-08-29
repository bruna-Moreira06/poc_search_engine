import sqlite3

def initialize_db():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('poc_search_engine.db')
    cursor = conn.cursor()

    # Lire et exécuter le script SQL
    with open('setup_db.sql', 'r') as f:
        sql_script = f.read()
    cursor.executescript(sql_script)

    # Fermer la connexion
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")

if __name__ == '__main__':
    initialize_db()
