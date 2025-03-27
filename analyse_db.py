import sqlite3

def get_db_structure(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Récupérer les noms des tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("⚠️ Aucune table trouvée dans la base de données.")
        return

    print("\n📂 **Structure de la base de données :**\n")

    for table in tables:
        table_name = table[0]
        print(f"📌 **Table : {table_name}**")

        # Récupérer les colonnes de la table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        print("   🏛 **Colonnes :**")
        for col in columns:
            col_id, col_name, col_type, not_null, default_value, primary_key = col
            pk_status = "🔑 (PK)" if primary_key else ""
            print(f"      - {col_name} ({col_type}) {pk_status}")

        # Récupérer les relations (clés étrangères)
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()

        if foreign_keys:
            print("   🔗 **Relations (Clés étrangères) :**")
            for fk in foreign_keys:
                # Vérifiez dynamiquement le nombre de colonnes retournées
                from_col = fk[1]
                ref_table = fk[2]
                ref_col = fk[3]
                on_update = fk[4] if len(fk) > 4 else "NO ACTION"
                on_delete = fk[5] if len(fk) > 5 else "NO ACTION"
                print(f"      - {from_col} → {ref_table}.{ref_col} (ON DELETE {on_delete}, ON UPDATE {on_update})")

        print("\n" + "-"*50 + "\n")

    conn.close()

# Exécuter l'analyse
get_db_structure("db.sqlite3")


