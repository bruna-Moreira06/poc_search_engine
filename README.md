# POC Search Engine

## Description

Ce projet est une application web simple qui permet de gérer des documents PDF en les indexant dans ElasticSearch et en fournissant une interface de recherche pour explorer ces documents. L'application permet de télécharger des fichiers PDF, de les traiter pour extraire le texte, de les stocker dans ElasticSearch, et de rechercher des documents via une interface web. Il est également possible de marquer un document comme "signé".

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/) (pour lancer ElasticSearch via Docker)
- [pipenv](https://pipenv.pypa.io/en/latest/) ou [virtualenv](https://virtualenv.pypa.io/en/latest/) pour créer un environnement virtuel (facultatif mais recommandé)

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/bruna-Moreira06/poc_search_engine.git
   cd poc_search_engine
   ```
2. Créez un environnement virtuel et activez-le :


   Avec virtualenv :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Avec pipenv :

   ```bash
   pipenv shell
   ```

3. Installez les dépendances requises :

```bash
pip install -r requirements.txt
```

4. Démarrez ElasticSearch via Docker :

   Créez un fichier docker-compose.yml avec le contenu suivant :

   ```yaml
   version: '3'
   services:
   elasticsearch:
   image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
   container_name: elasticsearch
   environment: - discovery.type=single-node - xpack.security.enabled=false
   ports: - "9200:9200" - "9300:9300"
   ```

   Puis, lancez ElasticSearch :

   ```bash
   docker-compose up -d
   ```

5. Initialisez la base de données SQLite :

Un script SQL est fourni pour créer la structure de la base de données. Exécutez les commandes suivantes pour initialiser la base de données :

```bash
python initialize_db.py
```
Ce script exécutera le fichier setup_db.sql et créera les tables nécessaires dans la base de données SQLite.

6. Lancez l'application Flask :

```bash
python app.py
```

7. Accédez à l'application dans votre navigateur à l'adresse suivante : http://localhost:5000

## Utilisation
### Téléchargement de PDF
Cliquez sur "Upload PDF" dans la page d'accueil.
Sélectionnez un fichier PDF depuis votre ordinateur.
Cliquez sur "Upload". Le fichier sera indexé dans ElasticSearch.
### Recherche de documents
Cliquez sur "Search Documents" dans la page d'accueil.
Entrez un mot-clé ou une phrase dans la barre de recherche.
Cliquez sur "Search" pour voir les résultats correspondants.
### Marquer un document comme signé
Après avoir effectué une recherche, cliquez sur "Mark as Signed" pour un document non signé. Le statut du document sera mis à jour dans ElasticSearch.
### Gestion des utilisateurs
Accédez à http://localhost:5000/add_user pour ajouter un nouvel utilisateur.
Remplissez le formulaire avec les informations de l'utilisateur et cliquez sur "Add User".
## Détails techniques
-  Flask : Utilisé pour créer l'application web.
-  PyMuPDF : Utilisé pour extraire du texte des fichiers PDF.
-  ElasticSearch : Utilisé pour indexer et rechercher des documents.
-  SQLite : Utilisé pour gérer les utilisateurs, les rôles, les permissions et l'étiquetage des documents.
-  Docker : Utilisé pour lancer ElasticSearch en tant que conteneur.

## Déploiement
Pour déployer cette application sur un serveur, vous pouvez envisager d'utiliser des plateformes comme Heroku, AWS, ou DigitalOcean. Assurez-vous d'adapter la configuration de Docker et de Flask pour un environnement de production.

## Contribution
Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter de changements majeurs.

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
