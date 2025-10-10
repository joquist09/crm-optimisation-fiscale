# CRM OF - Application Web Django

**Application CRM (Customer Relationship Management) pour la gestion des conseillers, clients, sociétés et enfants avec un design élégant en bleu marin foncé, gris pâle et or pâle.**

## 🚀 Installation et Démarrage Rapide

### Prérequis
- Python 3.8+
- Windows PowerShell

### 1. Cloner et configurer l'environnement

```powershell
# Naviguer vers le dossier du projet
cd "C:\Users\JordanQuist\OneDrive - SFLDFSI\Documents\OF"

# Créer et activer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configurer la base de données

```powershell
# Appliquer les migrations
python manage.py migrate

# (Optionnel) Créer un superutilisateur pour l'admin Django
python manage.py createsuperuser
```

### 3. Démarrer le serveur

```powershell
python manage.py runserver
```

L'application sera accessible à l'adresse : **http://127.0.0.1:8000/**

---

## 🎨 Design et Interface

### Palette de couleurs
- **Bleu marin foncé** (#1a365d) : Navigation, en-têtes
- **Gris pâle** (#f7f9fc) : Arrière-plan principal
- **Or pâle** (#f6f3e7) : Éléments de mise en évidence
- **Or accent** (#d4af37) : Boutons et accents

### Caractéristiques visuelles
- Design responsive avec Bootstrap 5
- Interface moderne avec des dégradés
- Icônes Font Awesome intégrées
- Effets de survol et transitions fluides
- Cartes avec ombres et coins arrondis

---

## 📋 Fonctionnalités CRM

### 🏠 Dashboard Principal
- Statistiques en temps réel (nombre de conseillers, clients, sociétés)
- Listes des derniers conseillers et clients créés
- Actions rapides pour création de nouveaux enregistrements
- Navigation intuitive avec sidebar

### 👔 Gestion des Conseillers
- **Liste** : Vue d'ensemble avec recherche et filtres
- **Création** : Formulaire complet (nom, prénom, email, téléphone, langue)
- **Détail** : Profil complet avec liste des clients assignés
- **Modification** : Édition de toutes les informations

### 👥 Gestion des Clients
- **Liste** : Affichage avec filtres par conseiller et recherche textuelle
- **Création** : Formulaire détaillé (informations personnelles, conseiller assigné)
- **Détail** : Vue complète avec sociétés et enfants associés
- **Modification** : Édition de toutes les données client

### 🏢 Gestion des Sociétés
- **Liste** : Vue des sociétés avec informations client et financières
- **Création** : Formulaire avec données financières détaillées
- **Détail** : Affichage spécialisé selon le type (opérante/gestion)
- **Modification** : Édition complète des informations

### 👶 Gestion des Enfants
- **Création** : Ajout depuis la page client
- **Modification** : Édition des informations de garde et coûts
- **Affichage** : Intégré dans la vue détail du client

---

## 🔧 Structure Technique

### Modèles de données
- **Conseiller** : Informations professionnelles et contact
- **Client** : Données personnelles complètes avec relations
- **Société** : Types opérante/gestion avec données financières
- **Enfant** : Informations de garde et coûts
- **+20 autres modèles** : Revenus, actifs, assurances, etc.

### Architecture
```
ofproject/               # Configuration Django
├── settings.py          # Configuration principale
├── urls.py             # Routage principal
└── wsgi.py             # Point d'entrée WSGI

core/                   # Application principale
├── models.py           # Modèles de données (35+ modèles)
├── views.py            # Vues métier
├── forms.py            # Formulaires Django
├── urls.py             # Routage de l'app
├── admin.py            # Interface d'administration
└── templates/core/     # Templates HTML
    ├── base.html       # Template de base avec design
    ├── dashboard.html  # Page d'accueil
    ├── *_list.html     # Pages de liste
    ├── *_detail.html   # Pages de détail
    └── *_form.html     # Pages de formulaires
```

---

## 📊 Utilisation Recommandée

### Workflow typique
1. **Créer des conseillers** dans le système
2. **Ajouter des clients** et les assigner aux conseillers
3. **Créer des sociétés** pour les clients qui en ont
4. **Ajouter des enfants** si nécessaire
5. **Utiliser la recherche** pour retrouver rapidement les informations

### Navigation efficace
- Utilisez la **sidebar** pour un accès rapide aux sections
- La **recherche** est disponible sur toutes les pages de liste
- Les **liens contextuels** permettent de naviguer entre entités liées
- Le **breadcrumb** aide à se repérer dans l'arborescence

---

## 🛠️ Développement et Personnalisation

### Ajouter de nouveaux modèles
1. Définir le modèle dans `core/models.py`
2. Créer les migrations : `python manage.py makemigrations`
3. Appliquer : `python manage.py migrate`
4. Ajouter les vues dans `core/views.py`
5. Créer les templates correspondants

### Personnaliser le design
- Modifier les variables CSS dans `core/templates/core/base.html`
- Ajuster les couleurs dans la section `:root`
- Personnaliser les composants Bootstrap selon les besoins

### Étendre les fonctionnalités
- Ajouter de nouveaux champs aux formulaires dans `core/forms.py`
- Créer de nouvelles vues métier dans `core/views.py`
- Développer des rapports et statistiques personnalisés

---

## 🔐 Sécurité et Production

### Pour un déploiement en production
1. Modifier `DEBUG = False` dans `settings.py`
2. Configurer une base de données robuste (PostgreSQL)
3. Ajouter l'authentification utilisateur
4. Implémenter les permissions et rôles
5. Configurer HTTPS et sécurité

### Sauvegarde des données
```powershell
# Exporter les données
python manage.py dumpdata > backup.json

# Importer les données
python manage.py loaddata backup.json
```

---

## 📞 Support et Maintenance

### Logs et débogage
- Les erreurs Django sont affichées dans la console de développement
- Utilisez `python manage.py check` pour vérifier la configuration
- Les logs sont disponibles dans la console du serveur

### Mise à jour
1. Sauvegarder les données existantes
2. Mettre à jour le code
3. Appliquer les nouvelles migrations si nécessaire
4. Redémarrer le serveur

---

## 🎯 Fonctionnalités Avancées Prêtes

Le système inclut déjà les modèles pour :
- Revenus (emploi, entreprise, dividendes, RRQ)
- Actifs et placements (REER, CELI, non enregistré)
- Assurances vie avec projections
- Informations fiscales (client et société)
- Fonds de pension (CD, RRE, PD)
- Budgets (permanent et extraordinaire)
- Flux monétaires et projections

Ces modèles peuvent être facilement intégrés dans l'interface selon les besoins futurs.

---

**🚀 L'application CRM OF est maintenant prête à l'utilisation !**
