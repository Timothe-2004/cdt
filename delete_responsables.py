import sqlite3

def supprimer_associations_responsables_classes():
    try:
        # Connexion à la base de données SQLite
        print("Connexion à la base de données...")
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print("Connexion réussie.")

        # Supprimer toutes les associations dans la table `classes_responsableclasse`
        print("Suppression des associations entre responsables et classes...")
        cursor.execute("DELETE FROM classes_responsableclasse;")

        # Valider les changements
        conn.commit()
        print("Toutes les associations ont été supprimées avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    finally:
        # Fermeture de la connexion
        if conn:
            conn.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    supprimer_associations_responsables_classes()