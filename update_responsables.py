import sqlite3

def associer_responsables_classes():
    try:
        # Connexion à la base de données SQLite
        print("Connexion à la base de données...")
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print("Connexion réussie.")

        # Exemple d'association : Associer chaque responsable à une classe spécifique
        associations = [
            (5, 1),  # Associer le responsable avec ID 5 à la classe avec ID 1
            (9, 2)   # Associer le responsable avec ID 9 à la classe avec ID 2
        ]

        # Vérification des IDs avant insertion
        print("Vérification des IDs des utilisateurs et des classes...")
        for user_id, classe_id in associations:
            cursor.execute("SELECT COUNT(*) FROM auth_user WHERE id = ?", (user_id,))
            user_exists = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM classes_classe WHERE id = ?", (classe_id,))
            classe_exists = cursor.fetchone()[0]

            if not user_exists:
                print(f"Utilisateur avec ID {user_id} n'existe pas.")
                continue
            if not classe_exists:
                print(f"Classe avec ID {classe_id} n'existe pas.")
                continue

            # Insérer les associations dans la table `classes_responsableclasse`
            try:
                cursor.execute(
                    "INSERT INTO classes_responsableclasse (user_id, classe_id) VALUES (?, ?)",
                    (user_id, classe_id)
                )
                print(f"Association ajoutée : Utilisateur {user_id} -> Classe {classe_id}")
            except sqlite3.IntegrityError as e:
                print(f"Erreur d'intégrité lors de l'insertion : {e}")

        # Valider les changements
        conn.commit()
        print("Associations ajoutées avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    finally:
        # Fermeture de la connexion
        if conn:
            conn.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    associer_responsables_classes()