# 🚀 Déploiement avec SQLite sur Render

## ✅ Avantages de SQLite

- **Simple**: Aucune base de données externe nécessaire
- **Rapide**: Déploiement en quelques minutes
- **Gratuit**: Pas de coûts supplémentaires
- **Fiable**: Parfait pour les applications de taille moyenne

## 📋 Étapes de déploiement

### 1. Préparer le repository
```bash
# Vérifier que tous les fichiers sont ajoutés
git add .

# Commit
git commit -m "Deploy with SQLite to Render"

# Push vers GitHub
git push origin main
```

### 2. Créer le service sur Render

1. **Allez sur [render.com](https://render.com)**
2. **Cliquez sur "New +" → "Web Service"**
3. **Connectez votre repository GitHub**
4. **Sélectionnez votre repository**

### 3. Configuration du service

- **Name**: `cahier-de-texte`
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn cahier_de_texte.wsgi:application`

### 4. Variables d'environnement

```
SECRET_KEY: [Généré automatiquement par Render]
DEBUG: False
ALLOWED_HOSTS: votre-app.onrender.com
```

> **Note**: Aucune variable `DATABASE_URL` nécessaire avec SQLite !

### 5. Déployer

1. **Cliquez sur "Create Web Service"**
2. **Attendez que le déploiement se termine** (2-3 minutes)
3. **Vérifiez les logs** pour voir le processus

## 🔑 Accès administrateur

Un superutilisateur est créé automatiquement :

- **URL Admin**: `https://votre-app.onrender.com/admin/`
- **Nom d'utilisateur**: `admin`
- **Mot de passe**: `admin123`
- **Email**: `admin@example.com`

> **⚠️ Important**: Changez ces identifiants après le premier déploiement !

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

## 🛠️ Dépannage

### Problèmes courants

#### 1. Erreur de build
- Vérifiez que `build.sh` est exécutable
- Vérifiez que `requirements.txt` contient toutes les dépendances
- Vérifiez les logs de build

#### 2. Erreur de base de données
- Vérifiez que les migrations s'exécutent correctement
- Vérifiez que le fichier `db.sqlite3` est créé
- Vérifiez les logs de migration

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
env | grep -E "(SECRET_KEY|DEBUG|ALLOWED_HOSTS)"

# Vérifier la configuration Django
python manage.py check --deploy
```

## 📊 Monitoring

### Surveiller l'application
- Vérifiez les logs régulièrement
- Surveillez les performances
- Vérifiez l'utilisation de la base de données

### Sauvegardes
- La base de données SQLite est sauvegardée automatiquement par Render
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

## 🚀 Déploiement rapide

1. **Fork** ce repository
2. **Connectez** votre repository à Render
3. **Configurez** les variables d'environnement
4. **Déployez** !

Votre application sera accessible à l'URL fournie par Render.

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs de Render
2. Consultez la documentation Django
3. Vérifiez la configuration des variables d'environnement

## 🎉 Félicitations !

Votre application Django est maintenant déployée sur Render avec SQLite !

- ✅ **Design moderne** avec Bootstrap 5
- ✅ **Interface responsive** pour tous les appareils
- ✅ **Base de données SQLite** simple et fiable
- ✅ **Déploiement automatique** avec Render
- ✅ **Superutilisateur** créé automatiquement
