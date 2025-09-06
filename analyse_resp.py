import sqlite3

def verifier_donnees_de_base():
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print("Connexion à la base de données réussie.")

        # Vérification des données dans les tables de base
        tables = ['auth_user', 'users_profilutilisateur', 'classes_responsableclasse', 'classes_classe']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Nombre d'entrées dans la table {table} : {count}")

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Fermeture de la connexion
        if conn:
            conn.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    verifier_donnees_de_base()


import sqlite3

def verifier_relations_de_base():
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print("Connexion à la base de données réussie.")

        # Requête simplifiée pour vérifier les relations de base
        query = """
        SELECT
            u.id AS responsable_id,
            u.username AS responsable_nom
        FROM
            auth_user u
        JOIN
            users_profilutilisateur pu ON u.id = pu.user_id
        WHERE
            pu.role = 'responsable_classe';
        """

        # Exécution de la requête
        cursor.execute(query)
        print("Requête exécutée avec succès.")

        # Récupération des résultats
        results = cursor.fetchall()
        print(f"Nombre de responsables de classe trouvés : {len(results)}")

        # Affichage des responsables
        for row in results:
            responsable_id, responsable_nom = row
            print(f"Responsable : {responsable_nom} (ID: {responsable_id})")

        # Requête pour obtenir les responsables de classes et les classes associées
        query = """
        SELECT
            u.id AS responsable_id,
            u.username AS responsable_nom,
            c.id AS classe_id,
            c.nom AS classe_nom
        FROM
            auth_user u
        JOIN
            classes_responsableclasse rc ON u.id = rc.user_id
        JOIN
            classes_classe c ON rc.classe_id = c.id
        ORDER BY
            u.username, c.nom;
        """

        print("\nAffichage des responsables et des classes associées :")
        cursor.execute(query)
        responsables_classes = cursor.fetchall()

        # Affichage des résultats
        current_responsable = None
        for row in responsables_classes:
            responsable_id, responsable_nom, classe_id, classe_nom = row
            if responsable_nom != current_responsable:
                print(f"\n📌 Responsable : {responsable_nom} (ID: {responsable_id})")
                current_responsable = responsable_nom
            print(f"   - Classe : {classe_nom} (ID: {classe_id})")

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Fermeture de la connexion
        if conn:
            conn.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    verifier_relations_de_base()


import sqlite3

def associer_responsables_classes():
    try:
        # Connexion à la base de données SQLite
        print("Connexion à la base de données...")
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print("Connexion réussie.")

        # Lister toutes les classes académiques disponibles
        print("\nListe des classes académiques disponibles :")
        cursor.execute("SELECT id, nom FROM classes_classe;")
        classes = cursor.fetchall()
        for classe_id, classe_nom in classes:
            print(f"Classe ID: {classe_id}, Nom: {classe_nom}")

        # Exemple d'association : Associer chaque responsable à une classe spécifique
        associations = [
            (5, 1),  # Associer le responsable avec ID 5 à la classe avec ID 1
            (9, 2)   # Associer le responsable avec ID 9 à la classe avec ID 2
        ]

        # Insérer les associations dans la table `classes_responsableclasse`
        for user_id, classe_id in associations:
            cursor.execute(
                "INSERT INTO classes_responsableclasse (user_id, classe_id) VALUES (?, ?)",
                (user_id, classe_id)
            )

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
