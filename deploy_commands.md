# 🚀 Commandes de Déploiement sur Render

## 📋 Checklist de déploiement

### 1. Préparation du repository
```bash
# Vérifier que tous les fichiers sont ajoutés
git status

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Deploy to Render - $(date)"

# Push vers GitHub
git push origin main
```

### 2. Configuration sur Render

#### A. Créer un Web Service
1. Allez sur [render.com](https://render.com)
2. Cliquez sur "New +" → "Web Service"
3. Connectez votre repository GitHub
4. Sélectionnez votre repository

#### B. Configuration du service
- **Name**: `cahier-de-texte`
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn cahier_de_texte.wsgi:application`

#### C. Variables d'environnement
```
SECRET_KEY: [Généré automatiquement par Render]
DEBUG: False
ALLOWED_HOSTS: votre-app.onrender.com
DATABASE_URL: [Généré automatiquement par la base de données]
```

### 3. Créer une base de données PostgreSQL
1. Cliquez sur "New +" → "PostgreSQL"
2. **Name**: `cahier-de-texte-db`
3. **Plan**: Free
4. Copiez l'URL de connexion

### 4. Connecter la base de données
1. Dans votre service web, ajoutez la variable d'environnement :
   - **Key**: `DATABASE_URL`
   - **Value**: URL de connexion de votre base de données

### 5. Déployer
1. Cliquez sur "Create Web Service"
2. Attendez que le déploiement se termine
3. Vérifiez les logs pour voir le processus

## 🔧 Commandes post-déploiement

### Créer un superutilisateur
```bash
# Via le shell de Render
python manage.py createsuperuser
```

### Vérifier les migrations
```bash
# Via le shell de Render
python manage.py showmigrations
```

### Collecter les fichiers statiques
```bash
# Via le shell de Render
python manage.py collectstatic --noinput
```

## 📱 URLs d'accès

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

## 🛠️ Dépannage

### Problèmes courants

#### 1. Erreur de build
- Vérifiez que `build.sh` est exécutable
- Vérifiez que `requirements.txt` contient toutes les dépendances
- Vérifiez les logs de build

#### 2. Erreur de base de données
- Vérifiez que `DATABASE_URL` est correctement configurée
- Vérifiez que la base de données est créée
- Vérifiez les migrations

#### 3. Erreur de fichiers statiques
- Vérifiez que `STATIC_ROOT` est configuré
- Vérifiez que `collectstatic` s'exécute correctement
- Vérifiez la configuration WhiteNoise

#### 4. Erreur de variables d'environnement
- Vérifiez que `SECRET_KEY` est configurée
- Vérifiez que `ALLOWED_HOSTS` contient votre domaine
- Vérifiez que `DEBUG` est False en production

### Logs utiles
```bash
# Voir les logs de l'application
# Via l'interface Render ou le shell

# Vérifier les variables d'environnement
env | grep -E "(SECRET_KEY|DEBUG|ALLOWED_HOSTS|DATABASE_URL)"

# Vérifier la configuration Django
python manage.py check --deploy
```

## 🔄 Mise à jour

### Pour mettre à jour l'application
```bash
# Modifier le code
# ...

# Commit et push
git add .
git commit -m "Update application"
git push origin main

# Render déploiera automatiquement
```

### Pour mettre à jour la base de données
```bash
# Via le shell de Render
python manage.py makemigrations
python manage.py migrate
```

## 📊 Monitoring

### Surveiller l'application
- Vérifiez les logs régulièrement
- Surveillez les performances
- Vérifiez l'utilisation de la base de données

### Sauvegardes
- La base de données est sauvegardée automatiquement par Render
- Considérez des sauvegardes supplémentaires pour les données critiques

## 🎯 Optimisations

### Performance
- Utilisez le cache pour les requêtes fréquentes
- Optimisez les requêtes de base de données
- Utilisez CDN pour les fichiers statiques

### Sécurité
- Gardez `SECRET_KEY` secrète
- Utilisez HTTPS en production
- Configurez les en-têtes de sécurité
- Limitez l'accès à l'admin Django
