#!/bin/bash

echo "🚀 Déploiement du Cahier de Texte Universitaire sur Render"
echo "=================================================="

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Assurez-vous d'être dans le répertoire racine du projet."
    exit 1
fi

echo "✅ Répertoire de projet détecté"

# Vérifier que Git est initialisé
if [ ! -d ".git" ]; then
    echo "❌ Erreur: Git n'est pas initialisé. Initialisez Git d'abord."
    exit 1
fi

echo "✅ Repository Git détecté"

# Ajouter tous les fichiers
echo "📁 Ajout des fichiers au repository..."
git add .

# Commit
echo "💾 Création du commit..."
git commit -m "Deploy to Render - $(date)"

# Push vers le repository distant
echo "🚀 Push vers le repository distant..."
git push origin main

echo ""
echo "✅ Déploiement terminé !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Allez sur https://render.com"
echo "2. Créez un nouveau Web Service"
echo "3. Connectez votre repository GitHub"
echo "4. Configurez les paramètres :"
echo "   - Build Command: ./build.sh"
echo "   - Start Command: gunicorn cahier_de_texte.wsgi:application"
echo "5. Créez une base de données PostgreSQL"
echo "6. Configurez les variables d'environnement"
echo "7. Déployez !"
echo ""
echo "🔗 Votre application sera accessible à l'URL fournie par Render"
