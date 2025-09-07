# Cahier de Texte Universitaire

Une application Django moderne pour la gestion des cours, séances et utilisateurs dans un environnement universitaire.

## 🚀 Déploiement sur Render

### Prérequis
- Compte Render.com
- Repository GitHub avec votre code

### Étapes de déploiement

#### 1. Préparer le repository
```bash
# Cloner votre repository
git clone <votre-repo-url>
cd cahier_de_texte

# Ajouter tous les fichiers de configuration
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### 2. Créer un service sur Render

1. **Connecter votre repository**
   - Allez sur [render.com](https://render.com)
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre repository GitHub

2. **Configuration du service**
   - **Name**: `cahier-de-texte`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn cahier_de_texte.wsgi:application`

3. **Variables d'environnement**
   ```
   SECRET_KEY: [Généré automatiquement par Render]
   DEBUG: False
   ALLOWED_HOSTS: votre-app.onrender.com
   DATABASE_URL: [Généré automatiquement par la base de données]
   ```

#### 3. Configuration de la base de données

L'application utilise **SQLite** par défaut, ce qui simplifie le déploiement :
- ✅ **Aucune base de données externe nécessaire**
- ✅ **Configuration automatique**
- ✅ **Parfait pour les applications de taille moyenne**

> **Note**: Si vous préférez PostgreSQL, vous pouvez ajouter la variable d'environnement `DATABASE_URL` avec l'URL de votre base de données PostgreSQL.

#### 4. Déployer

1. **Déploiement automatique**
   - Render déploiera automatiquement votre application
   - Surveillez les logs pour voir le processus

2. **Créer un superutilisateur**
   ```bash
   # Via le shell de Render
   python manage.py createsuperuser
   ```

## 📱 Accès aux pages

### URLs principales
- **Page d'accueil**: `https://votre-app.onrender.com/`
- **Admin Django**: `https://votre-app.onrender.com/admin/`
- **Connexion**: `https://votre-app.onrender.com/accounts/login/`

### Pages de l'application
- **Dashboard**: `https://votre-app.onrender.com/users/dashboard/`
- **Liste des cours**: `https://votre-app.onrender.com/cours/`
- **Liste des formations**: `https://votre-app.onrender.com/formations/`
- **Liste des séances**: `https://votre-app.onrender.com/seances/`
- **Liste des classes**: `https://votre-app.onrender.com/classes/`

## 🛠️ Commandes utiles

### Développement local
```bash
# Installer les dépendances
pip install -r requirements.txt

# Migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer le serveur
python manage.py runserver
```

### Production (Render)
```bash
# Via le shell de Render
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 🔧 Configuration

### Variables d'environnement
- `SECRET_KEY`: Clé secrète Django (générée automatiquement)
- `DEBUG`: Mode debug (False en production)
- `ALLOWED_HOSTS`: Domaines autorisés
- `DATABASE_URL`: URL de connexion à la base de données

### Fichiers de configuration
- `requirements.txt`: Dépendances Python
- `Procfile`: Commande de démarrage
- `build.sh`: Script de build
- `runtime.txt`: Version de Python
- `render.yaml`: Configuration Render

## 📊 Fonctionnalités

### Gestion des utilisateurs
- Authentification et autorisation
- Rôles : Administrateur, Enseignant, Contrôleur, etc.
- Dashboards personnalisés

### Gestion des cours
- Création et modification des cours
- Affectation aux classes
- Gestion des crédits et volumes horaires

### Gestion des séances
- Planification des séances
- Suivi des présences
- Cahier de texte numérique

### Gestion des formations
- Création des formations
- Association avec les départements
- Gestion des responsables

## 🎨 Design

L'application utilise :
- **Bootstrap 5** pour l'interface utilisateur
- **Font Awesome** pour les icônes
- **Design responsive** pour tous les appareils
- **Interface moderne** et professionnelle

## 🔒 Sécurité

- Protection CSRF
- Validation des formulaires
- Gestion des permissions
- Variables d'environnement sécurisées

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs de Render
2. Consultez la documentation Django
3. Vérifiez la configuration des variables d'environnement

## 🚀 Déploiement rapide

1. **Fork** ce repository
2. **Connectez** votre repository à Render
3. **Créez** une base de données PostgreSQL
4. **Configurez** les variables d'environnement
5. **Déployez** !

Votre application sera accessible à l'URL fournie par Render.
