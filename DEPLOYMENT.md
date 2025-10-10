# Guide de Déploiement

## Option 1: Déploiement sur Render (Recommandé - Gratuit)

### Étapes:

1. **Créer un compte sur [Render.com](https://render.com)**

2. **Pousser votre code sur GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/VOTRE-USERNAME/crm-of.git
   git push -u origin main
   ```

3. **Créer un nouveau Web Service sur Render:**
   - Connectez votre repository GitHub
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn ofproject.wsgi:application`

4. **Variables d'environnement à configurer:**
   ```
   SECRET_KEY=django-insecure-VOTRE-CLE-SECRETE-ALEATOIRE-DE-50-CARACTERES
   DEBUG=False
   ALLOWED_HOSTS=votre-app-name.onrender.com
   ```

## Option 2: Déploiement sur Railway

1. **Aller sur [Railway.app](https://railway.app)**
2. **Connecter GitHub et sélectionner votre repo**
3. **Variables d'environnement:**
   ```
   SECRET_KEY=django-insecure-VOTRE-CLE-SECRETE
   DEBUG=False
   ```

## Option 3: Déploiement sur PythonAnywhere

1. **Créer un compte sur [PythonAnywhere](https://pythonanywhere.com)**
2. **Uploader votre code**
3. **Configurer l'application web Django**

## Génération d'une clé secrète

Utilisez cette commande pour générer une clé secrète sécurisée:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Test après déploiement

1. Accédez à votre URL de déploiement
2. L'application devrait afficher le dashboard
3. Testez la création de conseillers, clients, etc.
4. Testez l'export CSV

## Dépannage

- **Erreur 500**: Vérifiez les variables d'environnement
- **Fichiers statiques manquants**: Assurez-vous que WhiteNoise est configuré
- **Base de données**: SQLite est incluse, les migrations se font automatiquement