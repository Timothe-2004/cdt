CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");

CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");

CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");

CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");

CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");

CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");

CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);

CREATE TABLE "users_entite" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "code" varchar(20) NOT NULL UNIQUE, "description" text NULL, "date_creation" datetime NOT NULL);

CREATE TABLE "users_departement" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "code" varchar(20) NOT NULL UNIQUE, "description" text NULL, "responsable_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "entite_id" bigint NOT NULL REFERENCES "users_entite" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "users_profilutilisateur" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "role" varchar(50) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "departement_id" bigint NULL REFERENCES "users_departement" ("id") DEFERRABLE INITIALLY DEFERRED, "entite_id" bigint NULL REFERENCES "users_entite" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "users_departement_responsable_id_29bf3719" ON "users_departement" ("responsable_id");

CREATE INDEX "users_departement_entite_id_6fc6c763" ON "users_departement" ("entite_id");

CREATE TABLE "classes_responsableclasse" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer unsigned NOT NULL CHECK ("user_id" >= 0), "classe_id" integer unsigned NOT NULL CHECK ("classe_id" >= 0));

CREATE TABLE "classes_classe_formations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "classe_id" bigint NOT NULL REFERENCES "classes_classe" ("id") DEFERRABLE INITIALLY DEFERRED, "formation_id" bigint NOT NULL REFERENCES "formations_formation" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE UNIQUE INDEX "classes_classe_formations_classe_id_formation_id_5512e1ee_uniq" ON "classes_classe_formations" ("classe_id", "formation_id");

CREATE INDEX "classes_classe_formations_classe_id_a3f65056" ON "classes_classe_formations" ("classe_id");

CREATE INDEX "classes_classe_formations_formation_id_3e7b36f2" ON "classes_classe_formations" ("formation_id");

CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

CREATE TABLE "cours_cours" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "code" varchar(20) NOT NULL UNIQUE, "volume_horaire_total" integer NOT NULL, "volume_theorie" integer NOT NULL, "volume_tp" integer NOT NULL, "volume_td" integer NOT NULL, "date_creation" datetime NOT NULL, "enseignant_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "cours_cours_classes" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cours_id" bigint NOT NULL REFERENCES "cours_cours" ("id") DEFERRABLE INITIALLY DEFERRED, "classe_id" bigint NOT NULL REFERENCES "classes_classe" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "cours_cours_formations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cours_id" bigint NOT NULL REFERENCES "cours_cours" ("id") DEFERRABLE INITIALLY DEFERRED, "formation_id" bigint NOT NULL REFERENCES "formations_formation" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "cours_cours_enseignant_id_c1d624c1" ON "cours_cours" ("enseignant_id");

CREATE UNIQUE INDEX "cours_cours_classes_cours_id_classe_id_846837f8_uniq" ON "cours_cours_classes" ("cours_id", "classe_id");

CREATE INDEX "cours_cours_classes_cours_id_d2241264" ON "cours_cours_classes" ("cours_id");

CREATE INDEX "cours_cours_classes_classe_id_bec07a06" ON "cours_cours_classes" ("classe_id");

CREATE UNIQUE INDEX "cours_cours_formations_cours_id_formation_id_ad41034e_uniq" ON "cours_cours_formations" ("cours_id", "formation_id");

CREATE INDEX "cours_cours_formations_cours_id_fb6e1b2b" ON "cours_cours_formations" ("cours_id");

CREATE INDEX "cours_cours_formations_formation_id_38a5b29d" ON "cours_cours_formations" ("formation_id");

CREATE INDEX "users_profilutilisateur_departement_id_968d9ade" ON "users_profilutilisateur" ("departement_id");

CREATE INDEX "users_profilutilisateur_entite_id_f5f534c0" ON "users_profilutilisateur" ("entite_id");

CREATE TABLE "formations_formation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "code" varchar(20) NOT NULL UNIQUE, "objectifs" text NULL, "credits" integer NOT NULL, "responsable_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "departement_id" bigint NULL REFERENCES "users_departement" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "formations_formation_responsable_id_0f2acedb" ON "formations_formation" ("responsable_id");

CREATE INDEX "formations_formation_departement_id_6e5a2e99" ON "formations_formation" ("departement_id");

CREATE TABLE "seances_seance" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_seance" date NOT NULL, "heure_debut" time NOT NULL, "heure_fin" time NOT NULL, "duree" bigint NOT NULL, "description" text NOT NULL, "statut" varchar(10) NOT NULL, "date_creation" datetime NOT NULL, "classe_id" bigint NOT NULL REFERENCES "classes_classe" ("id") DEFERRABLE INITIALLY DEFERRED, "cours_id" bigint NOT NULL REFERENCES "cours_cours" ("id") DEFERRABLE INITIALLY DEFERRED, "enseignant_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "responsable_classe_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "seances_historiquevalidation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_action" datetime NOT NULL, "action" varchar(20) NOT NULL, "validee_par_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "seance_id" bigint NOT NULL REFERENCES "seances_seance" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "seances_seance_classe_id_bcd92625" ON "seances_seance" ("classe_id");

CREATE INDEX "seances_seance_cours_id_f2b5236f" ON "seances_seance" ("cours_id");

CREATE INDEX "seances_seance_enseignant_id_73e0b963" ON "seances_seance" ("enseignant_id");

CREATE INDEX "seances_seance_responsable_classe_id_55bdfd24" ON "seances_seance" ("responsable_classe_id");

CREATE INDEX "seances_historiquevalidation_validee_par_id_8832aa92" ON "seances_historiquevalidation" ("validee_par_id");

CREATE INDEX "seances_historiquevalidation_seance_id_4f3616ab" ON "seances_historiquevalidation" ("seance_id");

CREATE TABLE "affectations_affectation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_affectation" datetime NOT NULL, "classe_id" bigint NOT NULL REFERENCES "classes_classe" ("id") DEFERRABLE INITIALLY DEFERRED, "cours_id" bigint NOT NULL REFERENCES "cours_cours" ("id") DEFERRABLE INITIALLY DEFERRED, "enseignant_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE UNIQUE INDEX "affectations_affectation_enseignant_id_cours_id_classe_id_8f310eb9_uniq" ON "affectations_affectation" ("enseignant_id", "cours_id", "classe_id");

CREATE INDEX "affectations_affectation_classe_id_05a4e883" ON "affectations_affectation" ("classe_id");

CREATE INDEX "affectations_affectation_cours_id_a604d93f" ON "affectations_affectation" ("cours_id");

CREATE INDEX "affectations_affectation_enseignant_id_9d81e0e2" ON "affectations_affectation" ("enseignant_id");

CREATE TABLE "classes_classe" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "code" varchar(20) NOT NULL UNIQUE, "annee_universitaire" varchar(9) NOT NULL, "effectif" integer unsigned NOT NULL CHECK ("effectif" >= 0), "date_creation" datetime NOT NULL, "entite_id_id" bigint NOT NULL REFERENCES "users_entite" ("id") DEFERRABLE INITIALLY DEFERRED, "responsable_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "est_tronc_commun" bool NOT NULL);

CREATE INDEX "classes_classe_entite_id_id_e9fb390c" ON "classes_classe" ("entite_id_id");

CREATE INDEX "classes_classe_responsable_id_07a1abfa" ON "classes_classe" ("responsable_id");

